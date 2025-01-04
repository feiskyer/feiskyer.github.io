---
author: "Derme"
date: 2024-06-25
linktitle: Triple Hyde Documentation
title: Triple Hyde Documentation
categories: [ "Development", "hugo" ]
tags: ["hugo", "theme", "html"]
weight: 10
---

# Partials

## Icon {#partials-icon}

Similar to the [icon shortcode]({{< ref "#shortcodes-icon" >}}), you can include icons in your own templates and partials by using Triple Hyde's `icon.html` partial. The partial takes one parameter which is the name of the icon to be included.

**Example:**

```go
  {{ partial "icon.html" "github" }}
```

Icons are populated using Hugo pipelines which makes them very flexible. Triple Hyde includes a number of built-in icons for social, links and other purposes. Check the [icon samples]({{< ref "icons" >}}) page for a full list of supported icons.

Custom icons can be added by providing your own icon assets in the `assets/icons/` directory of your project. The icon can then be referenced in the partial by using the SVG filename without the `.svg` extension.z

Icons can also be used in article content by calling the [icon shortcode]({{< ref "#shortcodes-icon" >}}).

<br/><br/><br/>

# Shortcodes

## Figure

`fig` allows you to add images with additional properties.

**Example:**

```md
{{</* fig class="full" src="https://derme.coffee/uploads/2023/07/twitter.png" title="Goodbye Twitter " link="https://derme.coffee/posts/2023-07-24-x/" */>}}
```

**Output:** {{< fig class="full" src="https://derme.coffee/uploads/2023/07/twitter.png" title="Goodbye Twitter" link="https://derme.coffee/posts/2023-07-24-x/" >}}

<br/><br/><br/>

## Icon {#shortcodes-icon}

`icon` outputs an SVG icon and takes the icon name as its only parameter. The icon is scaled to match the current text size.

**Example:**

```md
{{</* icon "github" */>}}
```

**Output:** {{< icon "github" >}}

Icons are populated using Hugo pipelines which makes them very flexible. Triple Hyde includes a number of built-in icons for social, links and other purposes. Check the [icon samples]({{< ref "icons" >}}) page for a full list of supported icons.

Custom icons can be added by providing your own icon assets in the `assets/icons/` directory of your project. The icon can then be referenced in the shortcode by using the SVG filename without the `.svg` extension.

Icons can also be used in partials by calling the [icon partial]({{< ref "#partials-icon" >}}).

<br/><br/><br/>

## Keyboard Input

`kbd` allows you to use the html `<kbd>` element to show keyboard input commands.

**Example:**

```md
{{</* kbd Ctrl */>}} + {{</* kbd R */>}} to refresh
```

**Output:** {{< kbd Ctrl >}} + {{< kbd R >}} to refresh

<br/><br/><br/>

## Note

`note` allows you to show a note in a box.

**Example:**

```md
{{</* note "Always keep documentation up to date" */>}}
```

**Output:** {{< note "Always keep documentation up to date" />}}

<br/><br/><br/>

## Warning

`warning` allows you to show a warning in a box.

**Example:**

```md
{{</* warning Always read the documentation before opening an GitHub issue */>}}
```

**Output:** {{< warning "Always read the documentation before opening an GitHub issue" />}}

<br/><br/><br/>
