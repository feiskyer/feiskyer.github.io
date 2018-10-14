# Changelog

__2018-09__

* Add _Table of Contents_ 
  * Configure using `.Site.Params.toc` with two possible value: "hugo" (using Hugo `{{ .TableOfContents }}`, and "tocbot" (using [Tocbot](https://tscanlin.github.io/tocbot/)), remove `.Site.Params.toc` to disable TOC
  * Change [_layouts/partials/header/styles.html_](https://github.com/htr3n/hyde-hyde/blob/master/layouts/partials/header/styles.html) to check `.Site.Params.toc` and add the corresponding styles
  * Change [_layouts/partials/page-single/content.html_](https://github.com/htr3n/hyde-hyde/blob/master/layouts/partials/page-single/content.html )  to add TOC per `.Site.Params.toc`
  * Add styles [_static-src/scss/hugo-toc.scss_](https://github.com/htr3n/hyde-hyde/blob/master/static-src/scss/hugo-toc.scss) and [_static-src/scss/tocbot.scss_](https://github.com/htr3n/hyde-hyde/blob/master/static-src/scss/tocbot.scss) that generate `hugo-toc.css` and `tocbot.css`, respectively
  * Tocbot can be configured in [_layouts/partials/page-single/footer.html_](_layouts/partials/page-single/footer.html_) with options as described in [its documentation](https://tscanlin.github.io/tocbot/#api)

__2018-07__

* Revise the shortcode ['fig.html'](https://github.com/htr3n/hyde-hyde/blob/master/layouts/shortcodes/fig.html)
* Rename `header/font-awesome.html` to `header/font-awesome-css.html` and adds [_footer/font-awesome-js.html_](https://github.com/htr3n/hyde-hyde/blob/master/layouts/partials/footer/font-awesome-js.html), uses Font-Awesome 5 deferred JavaScript loading to reduce CSS rendering blocking
* Refactor and consolidate all responsive breakpoints and creates a new style  [_\_responsive.scss_](static-src/scss/hyde-hyde/_responsive.scss)
* Refactor portfolio's projects into [_\_project.scss_](https://github.com/htr3n/hyde-hyde/blob/master/static-src/scss/hyde-hyde/_project.scss)
* Refactor styles for a list of posts into [_\_list.scss_](https://github.com/htr3n/hyde-hyde/blob/master/static-src/scss/hyde-hyde/_list.scss)
* Refactor misc. styles into [_\_misc.scss_](https://github.com/htr3n/hyde-hyde/blob/master/static-src/scss/hyde-hyde/_misc.scss)
* Remove  [_\_customised.scss_](https://github.com/htr3n/hyde-hyde/blob/master/static-src/scss/hyde-hyde/_customised.scss)

__Version 2.0__

* The main styles are refactored and redeveloped using SCSS (see [_static-src/scss_](https://github.com/htr3n/hyde-hyde/tree/v2.0.0/static-src/scss))
  and we no longer need `poole.css` and `hyde.css` because `hyde-hyde.scss` already incorporates relevant elements
  * `Hyde-hyde` can be customised by changing SCSS styles in [_static-src/scss/hyde-hyde_](https://github.com/htr3n/hyde-hyde/tree/v2.0.0/static-src/scss/hyde-hyde) and layouts in [_layouts_](https://github.com/htr3n/hyde-hyde/tree/v2.0.0/layouts) 
  * To generate `hyde-hyde.css`, please use any SCSS compiler to compile the main file  `hyde-hyde.scss`
* Restructure/modularise further the layouts (see [_layouts_](https://github.com/htr3n/hyde-hyde/tree/v2.0.0/layouts))
* Add '[_Portfolio_](https://github.com/htr3n/hyde-hyde/tree/v2.0.0/layouts/portfolio)' page inspired by Xiaoying Riley ([@3rdwave_themes](https://twitter.com/3rdwave_themes)) [Developer-Theme](https://github.com/xriley/developer-theme)
* Change the main body font to use system fonts (see [_\_variables.scss_](https://github.com/htr3n/hyde-hyde/tree/v1.0.0/static-src/scss/hyde-hyde/_variables.scss))
	* In case you prefer Web fonts, just include the template "[web-fonts.html](https://github.com/htr3n/hyde-hyde/tree/v2.0.0/layouts/partials/header/web-fonts.html)" to "[header.html](https://github.com/htr3n/hyde-hyde/tree/v2.0.0/layouts/partials/header.html)"
* Switch to main fixed width font [Source Code Pro](https://fonts.google.com/specimen/Source+Code+Pro)
* Add OpenGraph and TwitterCard templates (for SEO)
* Add '_Related Articles_' (see [_layouts/partials/post-related.html_](https://github.com/htr3n/hyde-hyde/tree/v2.0.0/layouts/partials/post-related.html))
* Add page navigation _NEXT / PREVIOUS_
* Switch datetime format to `"Jan 02 '06"` in the list of posts (see [_layouts/partials/post-list.html_](https://github.com/htr3n/hyde-hyde/tree/v2.0.0/layouts/partials/post-list.html)) to save some space
* Change styles for links, tags, text
* Add some handy shortcodes for `<kbd></kbd>` and `<blockquote></blockquote>`
* The License under '_Some Rights Reversed_' in the sidebar is switched from [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/) to [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

__Version 1.0__

* Color tones and layouts are inspired by [Nate Finch's blog](https://npf.io)
* Restructure/modularise the layouts (see [`layouts/_default/baseof.html`](https://github.com/htr3n/hyde-hyde/tree/v1.0.0/layouts/_default/baseof.html), [`layouts/_default/single.html`](https://github.com/htr3n/hyde-hyde/tree/v1.0.0/layouts/_default/single.html), [`layouts/_default/list.html`](https://github.com/htr3n/hyde-hyde/tree/v1.0.0/layouts/_default/list.html) and [`layouts/partials`](https://github.com/htr3n/hyde-hyde/tree/v1.0.0/layouts/partials/))
* Use [highlight.js](https://highlightjs.org) for code highlighting
* Use [Font-Awesome 5](https://fontawesome.com)'s icons
* Use main font [Fira-Sans](https://fonts.google.com/specimen/Fira+Sans) + fixed width font [Roboto Mono](https://fonts.google.com/specimen/Roboto+Mono)
* Add [GraphComment](https://graphcomment.com) for replacing the built-in [Disqus](https://disqus.com)
* Fork from [Hyde](https://github.com/spf13/hyde) 
* Refactor `basedof.html` and corresponding pages `index.html`, `single.html`, `list.html`
    - define blocks `content` and `footer` that will be fulfilled by each different type of layout.
