---
title: "用 Claude Code 处理视频太麻烦,我顺手写了个 Skill"
date: 2026-04-15T10:00:00+08:00
draft: false
tags: [Claude Code, Skills, 视频处理, AI 工具]
description: "介绍开源项目 video-skills：用 Claude Code 一句话完成视频下载、字幕转录和自动配音。详解 download-video、transcribe-video、narrate-video 三个 Skill 的安装方法与两个实战场景，让处理 YouTube、Bilibili 等平台视频变得轻松高效。"
---

看 YouTube 上的技术演讲，遇到讲得特别好的，想把要点记下来。以前的流程是：先找个在线工具下载视频，再找个工具提取字幕，字幕格式乱七八糟还得手动清理。一套下来，光找工具就花了半小时，笔记还没开始写。

另一个场景更折腾。录完一段产品 DEMO，画面有了，但没有解说，自己录需要反复调节奏。每次都在想，Claude Code 能帮我写代码，为什么不能帮我处理这些视频的活？

想了想，干脆自己写一个。

## 于是就有了 video-skills

video-skills 是我开源的一个视频处理 Skill 集合，包含三个技能：

- `download-video`：从 YouTube、Bilibili、Twitter/X 等 1000 多个平台下载视频
- `transcribe-video`：提取视频字幕，优先走内嵌字幕，没有才调 API 去转录
- `narrate-video`：给视频自动生成配音，画面和语音节奏对齐

三个技能可以单独用，也可以串起来。比如我最常用的流程是：下载一个 YouTube 视频 → 转成文字 → 拿着文字稿去做笔记整理。或者录完一段 DEMO → 让 Claude 看着画面写解说词 → 生成配音合进视频。

安装有两种方式。在 Claude Code 里直接：

```bash
/plugin marketplace add feiskyer/video-skills
/plugin install video-skills@video-skills
```

或者用 npx：

```bash
npx skills add feiskyer/video-skills
```

前置依赖就两个：`yt-dlp` 和 `ffmpeg`，macOS 用 Homebrew 装就行：

```bash
brew install yt-dlp ffmpeg
```

其他平台可以让 AI 帮你自动安装。

下面按我自己最常用的两个场景，看看它们的用法。

## 场景一：YouTube 视频变文字笔记

上周看到 Andrej Karpathy 一个新访谈，一个多小时，想先拿到文字稿挑重点看。打开 Claude Code，把链接丢进去：

```
帮我下载这个视频 https://www.youtube.com/watch?v=kwSVtQ7dziU
```

`download-video` 会用 yt-dlp 把视频拉下来，存到 `~/Downloads/Videos/`。只要音频、指定 720p 这些，直接用自然语言说就行。

下载完接着转文字：

```
把刚下载的视频转成文字
```

`transcribe-video` 会先检查视频有没有内嵌字幕。YouTube 上很多视频自带字幕，质量比语音识别好，速度快，关键是不花 API 的钱。只有没字幕的时候才走 OpenAI 的 `gpt-4o-transcribe`。转出来的文字稿自动清理了时间戳和格式标签，直接就是干净的纯文本。拿到文字稿再让 Claude 做个摘要，整个流程一气呵成。

没有内嵌字幕的视频需要配置 API Key，创建 `~/.transcribe_video.env`：

```bash
OPENAI_API_KEY=your-key-here
```

也支持其他兼容 OpenAI API 的平台，加上 `OPENAI_API_BASE` 就行。

不过下载和转录只解决了看视频的问题。如果你还需要编辑视频呢？比如录了个产品 DEMO，画面有了，但没声音。

## 场景二：录完 DEMO 自动配音

以前自己录个视频 DEMO，经常出现口误、卡壳、节奏不对等等的问题，录完还要花很长时间去剪辑，折腾半天才能搞定。

现在录好视频，直接一句话就可以搞定配音问题：

```
给这个 DEMO 视频加上中文配音 demo.mp4
```

Claude Code 会先每隔几秒截帧，看每个时间点屏幕上在发生什么，建一个场景时间表。然后根据画面写带时间戳的解说词，每段文字量只占时间窗口的 80% ，段落之间自然留白。最后调 Azure TTS 逐段生成语音，按时间戳合成到视频里。

不过使用时需要注意，配置 Azure 密钥，创建 `~/.narrate_video.env` 并设置：

```bash
AZURE_SPEECH_KEY=your-key-here
AZURE_SPEECH_REGION=eastus
```

## 写在最后

video-skills 做的事情其实并不复杂，只是把 yt-dlp、ffmpeg、还有 Azure Speech 这些命令行工具和 AI 调用包进了 Skill，但用起来的流畅度完全不一样。感兴趣的话可以直接安装来试试：`npx skills add feiskyer/video-skills`。

video-skills GitHub 为 <https://github.com/feiskyer/video-skills，有任何问题欢迎贡献完善>。
