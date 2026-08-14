---
title: "懒人神器！Gemini 一句话帮你做 PPT"
date: 2025-11-04T19:00:00+08:00
draft: false
tags: [AI, Vibe Coding, Gemini]
description: "Google Gemini 借助 Canvas 模式支持一句话自动生成 PPT，上传网络文章或学术论文即可提取要点生成幻灯片并导出到 Google Slides，本文实测其效果、风格与图表不能自动嵌入等使用细节。"
---

Google Gemini 支持通过 AI 一键自动生成 PPT 演示文档了，用起来挺方便的，分享给需要的同学。

试了下拿网络文章、学术论文等材料转 PPT，效果还不错。比起自己用 PowerPoint 一张一张做幻灯片，可以省下不少时间。

## 怎么使用？

打开 Gemini（需要订阅 Edu、Pro、Ultra 或者 Business），开启 Canvas 模式。上传你的文档，或者直接描述想做什么主题的 PPT。

比如我上传了《Context Engineering 2.0: The Context of Context Engineering》这篇论文，提示词就一句：

```
create a presentation based on attached doc
```

稍等一会，Gemini 就帮我做好了一个介绍上下文工程 2.0 的 PPT。默认的简洁风格我挺喜欢的，米黄色背景配深蓝色标题，看着舒服。

![上传文档并生成](/images/07a47e7d-a145-4396-bfb7-f82b21adbca8.png)

内容提取还算准确。比如论文里讲的“四个 Context Engineering 时代”，它会自动生成对应的页面。不过有个问题是，PDF 里的图表和示意图不会自动嵌入到 PPT 中。Gemini 只会提取文字内容，图片得自己加。

![生成的 PPT 内容](/images/efff4318-56ca-480f-b614-8736440c1d81.png)

而对应论文中的图片如下所示：

![PDF 中的图表内容](/images/4a242479-e3d9-4704-93bf-1265d77108f3.png)

**导出到 Google Slides**

点击右上角的"Export to Slides"按钮，直接导出到 Google 幻灯片中。

![导出到 Google Slides](/images/aa849cd6-d95f-4063-9848-247da6328984.png)

导出后就可以在 Google Slides 里继续编辑了。这时候补上原文里的图片，或者调整一下排版。

**中文支持**

中文内容也完全没问题，可以在草稿上继续提示让 Gemini 修改语言，比如“转化成中文 PPT”：

![支持中文内容](/images/f951d11b-8dcf-4200-b537-bba1f5280ca7.png)

## 一些小坑和建议

用下来主要有这么几点小坑和建议需要你注意：

1. **图片不会自动嵌入**：如果图片是网络链接的话，可以让 Gemini 直接插入。但 PDF 或文档里的图片不会直接放进 PPT，得导出后手动添加。

2. **适合快速起草**：如果需要基于一篇文章或想法快速做个 PPT 大纲，这个功能很实用。细节调整还是要靠人工。

3. **简洁风格为主**：目前生成的风格比较简单，就是简洁商务风。想要花哨的模板，还得自己改。

4. **支持多语言**：中英文都可以，提示词和生成内容都支持。

如果你需要经常做各种 PPT 的话，这个功能建议用起来。起码框架和内容提取它能搞定，剩下的再手动调就快多了。

---

**相关资源：**

- Gemini 官网：<https://gemini.google.com>
- Google Workspace 更新公告：<https://workspaceupdates.googleblog.com/2025/10/generate-presentations-in-gemini-app.html>

---

欢迎长按下面的二维码关注 **Feisky** 公众号，了解更多云原生和 AI 知识。

![](/images/mp.png)
