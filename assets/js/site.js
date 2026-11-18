/* Feisky: the whole site's script. Everything here answers something the
   reader does (scrolling, hovering, typing, clicking); nothing is required
   to read the site. */
(function () {
  "use strict";

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  /* ---- Article: reading progress + table of contents ---- */
  function article() {
    var prose = $("#prose");
    if (!prose) { return; }
    var bar = $("#progress");
    var toc = $("#toc");
    var links = toc ? $$("nav a", toc) : [];
    var wide = window.matchMedia("(min-width: 66rem)");

    /* The contents list is a sticky rail on wide screens and a collapsed
       disclosure above the text on narrow ones. */
    function syncToc() { if (toc) { toc.open = wide.matches; } }
    syncToc();
    if (wide.addEventListener) { wide.addEventListener("change", syncToc); }

    var targets = links.map(function (a) {
      var id = decodeURIComponent((a.getAttribute("href") || "").replace(/^#/, ""));
      var el = id ? document.getElementById(id) : null;
      return el ? { link: a, el: el } : null;
    }).filter(Boolean);

    var active = null;
    function update() {
      if (bar) {
        var rect = prose.getBoundingClientRect();
        var span = rect.height - window.innerHeight;
        var pct = span > 0 ? Math.min(1, Math.max(0, -rect.top / span)) : (rect.top <= 0 ? 1 : 0);
        bar.style.transform = "scaleX(" + pct.toFixed(4) + ")";
      }
      var current = null;
      for (var i = 0; i < targets.length; i++) {
        if (targets[i].el.getBoundingClientRect().top <= 120) { current = targets[i].link; }
      }
      if (current !== active) {
        if (active) { active.classList.remove("is-active"); }
        if (current) { current.classList.add("is-active"); }
        active = current;
      }
    }

    var ticking = false;
    function onScroll() {
      if (ticking) { return; }
      ticking = true;
      window.requestAnimationFrame(function () { update(); ticking = false; });
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    update();
  }

  /* ---- Article: copy buttons on code blocks ---- */
  function codeBlocks() {
    if (!navigator.clipboard) { return; }
    $$(".prose pre").forEach(function (pre) {
      var block = pre.parentNode.classList.contains("highlight") ? pre.parentNode : pre;
      var wrap = document.createElement("div");
      wrap.className = "codeblock";
      block.parentNode.insertBefore(wrap, block);
      wrap.appendChild(block);

      var button = document.createElement("button");
      button.type = "button";
      button.className = "codeblock__copy";
      button.textContent = "复制";
      button.addEventListener("click", function () {
        navigator.clipboard.writeText(pre.innerText.replace(/\n$/, "")).then(function () {
          button.textContent = "已复制";
          setTimeout(function () { button.textContent = "复制"; }, 1600);
        }, function () {
          button.textContent = "复制失败";
          setTimeout(function () { button.textContent = "复制"; }, 1600);
        });
      });
      wrap.appendChild(button);
    });
  }

  /* ---- Archive: filter the index as you type ---- */
  function filter() {
    var box = $("#filter");
    var input = $("#filter-input");
    if (!box || !input) { return; }
    var status = $("#filter-status");
    var empty = $("#filter-empty");
    var groups = $$("[data-group]").map(function (group) {
      return {
        el: group,
        entries: $$("[data-entry]", group).map(function (entry) {
          return { el: entry, text: (entry.textContent + " " + (entry.getAttribute("data-tags") || "")).toLowerCase() };
        })
      };
    });
    box.hidden = false;

    function apply() {
      var words = input.value.toLowerCase().split(/\s+/).filter(Boolean);
      var shown = 0;
      groups.forEach(function (group) {
        var any = false;
        group.entries.forEach(function (entry) {
          var match = words.every(function (w) { return entry.text.indexOf(w) !== -1; });
          entry.el.hidden = !match;
          if (match) { any = true; shown++; }
        });
        group.el.hidden = !any;
      });
      if (status) { status.textContent = words.length ? "匹配 " + shown + " 篇" : ""; }
      if (empty) { empty.hidden = shown !== 0; }
    }
    input.addEventListener("input", apply);
    if (input.value) { apply(); }
  }

  /* ---- Home: name the post under the pointer ---- */
  function skyline() {
    var root = $("#skyline");
    if (!root) { return; }
    var tip = $(".skyline__tip", root);
    if (!tip) { return; }

    function show(bar) {
      tip.textContent = bar.getAttribute("data-t");
      tip.hidden = false;
      var box = root.getBoundingClientRect();
      var bars = bar.parentNode.getBoundingClientRect();
      var at = bar.getBoundingClientRect();
      var left = at.left - box.left + at.width / 2 - tip.offsetWidth / 2;
      left = Math.max(0, Math.min(left, box.width - tip.offsetWidth));
      tip.style.left = left + "px";
      tip.style.top = (bars.top - box.top - tip.offsetHeight - 8) + "px";
    }
    root.addEventListener("mouseover", function (e) {
      var bar = e.target.closest ? e.target.closest("a[data-t]") : null;
      if (bar) { show(bar); }
    });
    root.addEventListener("mouseleave", function () { tip.hidden = true; });
  }

  function init() { article(); codeBlocks(); filter(); skyline(); }
  if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", init); } else { init(); }
})();
