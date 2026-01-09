#!/usr/bin/env python3
"""
Markdown Image Localizer

This script parses markdown files, downloads external images,
saves them locally with UUID-based names, and updates the markdown
to reference the local copies.

Usage:
    python download_images.py <markdown_file_or_dir> [more...]
    python download_images.py content/posts/my-post.md
    python download_images.py content/posts
    python download_images.py
"""

import re
import shutil
import sys
import uuid
from pathlib import Path
from urllib.parse import urlparse, unquote

import requests


# Regex pattern to match markdown images: ![alt](url)
# Captures: group(1)=alt text, group(2)=url, group(3)=optional title
IMAGE_PATTERN = re.compile(
    r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)'
)

# Directory where images will be saved (relative to blog root)
STATIC_IMAGES_DIR = Path("static/images")

# URL prefix for the saved images in markdown
IMAGE_URL_PREFIX = "/images"

VALID_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".svg",
    ".bmp",
    ".ico",
}


def get_file_extension(url: str, content_type: str | None = None) -> str:
    """
    Determine the file extension from URL or Content-Type header.

    Args:
        url: The image URL
        content_type: Optional Content-Type header value

    Returns:
        File extension including the dot (e.g., '.jpg')
    """
    # Try to get extension from URL path
    parsed = urlparse(url)
    path = unquote(parsed.path)

    # Handle URLs with query parameters
    if '?' in path:
        path = path.split('?')[0]

    ext = Path(path).suffix.lower()

    if ext in VALID_IMAGE_EXTENSIONS:
        return ext

    # Fallback to Content-Type header
    if content_type:
        content_type_map = {
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'image/webp': '.webp',
            'image/svg+xml': '.svg',
            'image/bmp': '.bmp',
            'image/x-icon': '.ico',
        }
        # Handle content-type with charset or other parameters
        mime_type = content_type.split(';')[0].strip().lower()
        if mime_type in content_type_map:
            return content_type_map[mime_type]

    # Default to .jpg if we can't determine
    return '.jpg'


def is_ignored_url(url: str) -> bool:
    """Return True for URLs that should be left untouched."""
    url = url.strip()

    # Skip data URLs
    if url.startswith('data:'):
        return True

    # Skip already-localized images
    if url.startswith(f"{IMAGE_URL_PREFIX}/"):
        return True

    parsed = urlparse(url)
    if parsed.scheme in ('http', 'https'):
        host = parsed.netloc.lower()
        if host in ('feisky.xyz', 'www.feisky.xyz'):
            return True

    return False


def is_remote_url(url: str) -> bool:
    """Return True if the URL is an HTTP(S) or protocol-relative URL."""
    parsed = urlparse(url)
    if parsed.scheme in ('http', 'https'):
        return True
    # Protocol-relative URL: //example.com/...
    return parsed.scheme == '' and parsed.netloc != ''


def normalize_remote_url(url: str) -> str:
    """Normalize protocol-relative URLs to https://."""
    if url.startswith('//'):
        return f"https:{url}"
    return url


def resolve_local_path(url: str, markdown_path: Path, blog_root: Path) -> Path:
    """Resolve a local image URL to a filesystem path."""
    parsed = urlparse(url)
    path = unquote(parsed.path)
    if path.startswith('/'):
        return blog_root / path.lstrip('/')
    return (markdown_path.parent / path).resolve(strict=False)


def download_image(url: str, save_dir: Path) -> tuple[Path, bool]:
    """
    Download an image from URL and save with a UUID-based filename.

    Args:
        url: The image URL to download
        save_dir: Directory to save the image

    Returns:
        Tuple of (saved_path, success)
    """
    try:
        # Set a reasonable timeout and user agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=30, stream=True)
        response.raise_for_status()

        # Determine file extension
        content_type = response.headers.get('Content-Type')
        ext = get_file_extension(url, content_type)

        # Generate UUID-based filename
        new_filename = f"{str(uuid.uuid4()).lower()}{ext}"
        save_path = save_dir / new_filename

        # Ensure directory exists
        save_dir.mkdir(parents=True, exist_ok=True)

        # Save the image
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"  ✓ Downloaded: {url[:60]}... -> {new_filename}")
        return save_path, True

    except requests.RequestException as e:
        print(f"  ✗ Failed to download {url}: {e}")
        return Path(), False
    except IOError as e:
        print(f"  ✗ Failed to save image: {e}")
        return Path(), False


def copy_local_image(src_path: Path, save_dir: Path) -> tuple[Path, bool]:
    """Copy a local image to the static images directory with a UUID name."""
    try:
        ext = src_path.suffix.lower()
        if ext not in VALID_IMAGE_EXTENSIONS:
            return Path(), False

        new_filename = f"{str(uuid.uuid4()).lower()}{ext}"
        save_path = save_dir / new_filename

        save_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, save_path)

        print(f"  ✓ Copied: {src_path} -> {new_filename}")
        return save_path, True
    except OSError as e:
        print(f"  ✗ Failed to copy image {src_path}: {e}")
        return Path(), False


def process_markdown_file(filepath: Path, dry_run: bool = False) -> tuple[int, int, int]:
    """
    Process a markdown file, downloading external images and updating references.

    Args:
        filepath: Path to the markdown file
        dry_run: If True, only show what would be done without making changes

    Returns:
        Tuple of (images_found, images_downloaded, images_copied)
    """
    # Determine the blog root (where static/ directory lives)
    # Assuming script is run from blog root or filepath is relative to it
    blog_root = Path.cwd()
    save_dir = blog_root / STATIC_IMAGES_DIR

    # Read the markdown content
    content = filepath.read_text(encoding='utf-8')

    # Find all image references
    matches = list(IMAGE_PATTERN.finditer(content))

    if not matches:
        return 0, 0, 0

    images_found = 0
    images_downloaded = 0
    images_copied = 0
    replacements = []

    for match in matches:
        url = match.group(2)

        images_found += 1

        if is_ignored_url(url):
            continue

        if dry_run:
            print(f"  [DRY RUN] Would localize: {url[:60]} ...")
            continue

        # Download or copy the image
        saved_path = Path()
        success = False
        if is_remote_url(url):
            download_url = normalize_remote_url(url)
            saved_path, success = download_image(download_url, save_dir)
            if success:
                images_downloaded += 1
        else:
            local_path = resolve_local_path(url, filepath, blog_root)
            if not local_path.exists():
                print(f"  ✗ Local image not found: {local_path}")
                continue
            saved_path, success = copy_local_image(local_path, save_dir)
            if success:
                images_copied += 1

        if success:
            # Build new markdown reference
            new_url = f"{IMAGE_URL_PREFIX}/{saved_path.name}"

            # Reconstruct the markdown image syntax
            new_image = f'![]({new_url})'

            replacements.append((match.group(0), new_image))

    # Apply replacements to content
    if replacements and not dry_run:
        new_content = content
        for old, new in replacements:
            new_content = new_content.replace(old, new, 1)

        # Write updated content
        filepath.write_text(new_content, encoding='utf-8')
        print(f"\n✓ Updated {filepath} with {len(replacements)} new image reference(s)")

    return images_found, images_downloaded, images_copied


def main():
    """Main entry point."""
    # Check for dry-run flag
    dry_run = '--dry-run' in sys.argv

    # Get file paths (excluding flags)
    filepaths = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    if not filepaths:
        filepaths = ['content/posts']

    expanded_paths: list[Path] = []
    for filepath_str in filepaths:
        path = Path(filepath_str)
        if path.is_dir():
            expanded_paths.extend(sorted(path.rglob("*.md")))
            expanded_paths.extend(sorted(path.rglob("*.markdown")))
        else:
            expanded_paths.append(path)

    if not expanded_paths:
        print(__doc__)
        print("\nError: No markdown files found to process.")
        sys.exit(1)

    total_found = 0
    total_downloaded = 0
    total_copied = 0

    for filepath in expanded_paths:

        if not filepath.exists():
            print(f"Error: File not found: {filepath}")
            continue

        found, downloaded, copied = process_markdown_file(filepath, dry_run=dry_run)
        total_found += found
        total_downloaded += downloaded
        total_copied += copied

    print(f"\n{'='*50}")
    print(
        f"Summary: Found {total_found} images, "
        f"downloaded {total_downloaded}, copied {total_copied}"
    )

    if dry_run:
        print("(Dry run - no changes made)")


if __name__ == '__main__':
    main()
