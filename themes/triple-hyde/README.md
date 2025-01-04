[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)](https://github.com/derme302/triple-hyde/blob/master/LICENSE.md) ![GitHub release](https://img.shields.io/github/release/derme302/triple-hyde.svg) ![GitHub stars](https://img.shields.io/github/stars/derme302/triple-hyde.svg) ![GitHub forks](https://img.shields.io/github/forks/derme302/triple-hyde.svg) ![GitHub issues](https://img.shields.io/github/issues/derme302/triple-hyde.svg) ![GitHub issues closed](https://img.shields.io/github/issues-closed/derme302/triple-hyde.svg)

# Triple-hyde

__`Triple-hyde`__ is a [Hugo](https://gohugo.io)'s theme that extends @htrn's [Hyde-hyde](https://github.com/htrn/hyde-hyde.git) theme that was originally derived from @spf13's [Hyde](https://github.com/spf13/hyde.git) and [Nate Finch's blog](https://npf.io). 

## Main changes

`hyde-hyde` has been paused in development for awhile, this fork implements the following changes:

* [PR #1](https://github.com/derme302/triple-hyde/pull/1) adds support for Google Analytics v4
* [PR #5](https://github.com/derme302/triple-hyde/pull/5) by [@eatingbrb](https://github.com/eatingbrb) adds support for Mastodon in social sidebar
* [PR #6](https://github.com/derme302/triple-hyde/pull/6) adds support for img shortcodes, allowing you to align an image inside of markdown by adding `#center`, `#left` or `#right` at the end of an image link. E.g. `![Metal](/uploads/2014/06/metal_icon.png#center)`
* [PR #7](https://github.com/derme302/triple-hyde/pull/7) correctly breaks out the about section on the sidebar as a partial
* [PR #8](https://github.com/derme302/triple-hyde/pull/8) updates theme to Font Awesome v6 and adds the Threads icon
* [PR #10](https://github.com/derme302/triple-hyde/pull/10) by [@MarcoIeni](https://github.com/MarcoIeni) adds support for [giscus](https://giscus.app/)
* [PR #11](https://github.com/derme302/triple-hyde/pull/11) adds internal Font Awesome 6 SVG Icon support and documentation from [Blowfish](https://blowfish.page)

For more details, please refer to [CHANGELOG](https://github.com/derme302/triple-hyde/blob/master/CHANGELOG.md).  A real site in action can be found [here](https://derme.coffee/) and the [example site](https://derme.coffee/triple-hyde) for reference.

## Usage

### Installation

__`triple-hyde`__ can be easily installed as many other Hugo themes:

```sh
$ cd HUGO_PROJECT

# then either clone hyde-hyde
$ git clone https://github.com/derme302/triple-hyde.git themes/triple-hyde

# or just add hyde-hyde as a submodule
$ git submodule add https://github.com/derme302/triple-hyde.git themes/triple-hyde
```

After that, choose `triple-hyde` as the main theme.

* `config.toml` 

```toml
theme = "triple-hyde"
```

* `config.yaml`

```yaml
theme : "triple-hyde"
```

That's all. You can render your site using `hugo` and see `triple-hyde` in action.

### Options

__`Triple-hyde`__ essentially inherits most of Hyde's [options](https://github.com/spf13/hyde#options). There are some extra options though

* `highlightjs = true`: use [highlight.js](https://highlightjs.org) instead of Hugo built-in support for code highlighting

  * `highlightjsstyle="highlight-style"`: only when `highlightjs = true`, please choose one of many _highlight.js_'s [styles](https://highlightjs.org/static/demo).
  * Since [v2.0.1](https://github.com/htr3n/hyde-hyde/tree/v2.0.1), highlighting for each page can be fine-tuned in the front matter, for example
    * `highlight = false`  (default `true`)
    * `highlightjslanguages = ["swift", "objectivec"]` 

* `postNavigation = true|false` (default `true`): Setting to `false` will disable the navigation _Previous Post_/ _Next Post_

* `relatedPosts = false|true` (default `false`): Setting to `true` allows related posts. Please refer [here](https://gohugo.io/content-management/related) for more details on related contents with Hugo.

* `GraphCommentId = "your-graphcomment-id"`: to use [GraphComment](https://graphcomment.com) instead of the built-in [Disqus](https://disqus.com). This option should be used exclusively with `disqusShortname = "disqus-shortname"`.

* `UtterancesRepo = "owner/repo-name"`: to use [Utterances](https://utteranc.es/) instead of the built-in [Disqus](https://disqus.com). This option should be used exclusively with `disqusShortname = "disqus-shortname"`.
  * `UtterancesIssueTerm = "pathname"` Method for Utterances to match issue's to posts (pathname, url, title, og:title)
  * `UtterancesTheme = "github-light"` Theme for Utterances (github-light, github-dark)

* `Commento = true`: to use [Commento](https://commento.io/) instead of the built-in [Disqus](https://disqus.com). This option should be used exclusively with `disqusShortname = "disqus-shortname"`.
  * `CommentoHost = "your-commento-instance"` [Self-hosted Commento](https://docs.commento.io/installation/self-hosting/) instance. This is not required if you're a [Commento.io](https://commento.io) user.

* `[params.social]`: in this section, you can set many social identities such as Twitter, Facebook, Github, Bitbucket, Gitlab, Instagram, LinkedIn, StackOverflow, Medium, Xing, Keybase.

  ```toml
  [params.social]
  	mastodon = "https://mastodon.gamedev.place/@derme302"
  	github = "derme302"
  	...
  ```
  
*  `include_toc = false`: Setting to `false` in FrontMatter will disable too short TOC data as your want. 

  * Per PR [#56](https://github.com/htr3n/hyde-hyde/commit/5ed13e17400bbc09a342b60fd50cd9fe3e6f1525), Gravatar pics can be used exclusively to `.Site.Params.authorimage` via the parameter `.Site.Params.social.gravatar`

    * ```toml
      [params.social]
      	gravatar = "your.email@domain.com"
      ```

### Customisations

* Most of the customisable SCSS styles in [_assets/scss/hyde-hyde_](https://github.com/derme302/triple-hyde/blob/master/assets/scss/triple-hyde) and Hugo templates in [_hyde-hyde/layouts_](https://github.com/derme302/triple-hyde/blob/master/layouts) are modularised and can be altered/adapted easily.

## Portfolio

Since version 2.0+, I added a portfolio page just in case. If you need it, simply add a menu section '_Portfolio_' in `config.toml` as following.

```toml
[[menu.main]]
    name = "Portfolio"
    identifier = "portfolio"
    weight = xyz
    url = "/portfolio/"
```

In the folder `content` , create a subfolder `portfolio` and use the following folder/content structure as reference.

```
$ tree portfolio
portfolio
├── _index.md
├── p1.md
├── p1.png
├── p2.md
├── p2.png
    ...
├── pn.md
└── pn.png
```

As I design the section _portfolio_ to be rendered as _list_,  `_index.md` can be used to set the title for your portfolio (you can read more about `_index.md` [here](https://gohugo.io/content-management/organization/#index-pages-index-md)). For instance, when I want to set the title of my portfolio "_Projects_", the front matter of `_index.md` will be:

```markdown
---
title: 'Projects'
---
```
The remaining of `_index.md` will be ignored.

For each project, just create a Markdown file with the following parameters in the front matter:

```markdown
---
title: "Project P1's Title"
description: "A short description"
date: '2018-01-02'
link: 'https://project-p1.com'
screenshot: 'p1.png'
layout: 'portfolio'
featured: true
---
Here is a longer summary of the project. You can write as long as you wish.
```

> __Note__:
>
> * `date` is important to sort the project chronologically
> * `layout 'portfolio'` is important as you don't want your project's page appear in the list of posts in the main page of your Web site but only in the _Portfolio_ ;)
> * `featured: true` : when you want to show a project as featured project. It is default to `false`. Note that only one project should be marked `featured: true` , otherwise, the result could be random as [the Hugo template](https://github.com/derme302/triple-hyde/blob/master/layouts/partials/portfolio/content.html) will take the first one.
> * The body of the Markdown file will be the summary of the project.

If you want to adjust the portfolio page to your needs, please have a look at the [main template](https://github.com/derme302/triple-hyde/blob/master/layouts/portfolio/list.html), that uses this [partial template](https://github.com/derme302/triple-hyde/blob/master/layouts/partials/portfolio/content.html) and [this SCSS style](https://github.com/derme302/triple-hyde/blob/master/assets/scss/triple-hyde/_project.scss).

### Posts in home page
By default hugo will show in your home page the most populated section.
This means that if you have more projects than posts, by default your home page will list your projects instead of your posts.
If you want to change this behaviour you can change the [mainsections](https://gohugo.io/functions/where/#mainsections).
For example, for the [exampleSite](https://github.com/derme302/triple-hyde/tree/master/exampleSite) this is how you should change the `config.toml` file:
```
[params]
    mainSections = ["posts"]
```

## Some Screenshots

### Main page

![hyde-hyde main screen](https://github.com/derme302/triple-hyde/raw/master/images/main.png)

### A post

![A post in hyde-hyde](https://github.com/derme302/triple-hyde/raw/master/images/post.png)

### Portfolio

![Portfolio hyde-hyde](https://github.com/derme302/triple-hyde/raw/master/images/portfolio.png)



### Mobile Mode with Collapsible Menu

<img src='https://github.com/derme302/triple-hyde/raw/master/images/mobile.png' alt='hyde-hyde in mobile mode' width='60%'>

## Author(s)

* `hyde-hyde` originally developed by [Alex T](https://github.com/htr3n)

* Original developed by [Mark Otto](https://github.com/mdo)

* Hugo's `hyde` ported by [Steve Francia](https://github.com/spf13)

## License

Open sourced under the [MIT license](LICENSE.md)
