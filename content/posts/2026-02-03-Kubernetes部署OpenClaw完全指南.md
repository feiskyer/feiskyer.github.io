---
title: "OpenClaw Kubernetes 部署完全指南：从单机到 7x24 服务"
date: 2026-02-03T10:01:00+08:00
draft: false
tags: [AI, OpenClaw, Kubernetes, 教程, 部署, 7x24, Helm, DevOps]
description: "手把手教你用 Kubernetes 与 Helm 把 OpenClaw 从本地单机部署为 7x24 全天候在线服务，涵盖 Telegram bot 配置、免费 LLM 模型接入、用户授权、配置持久化以及版本升级回滚。"
---

上周的 [[history/2026-01-30-OpenClaw 极简部署指南.md|OpenClaw 极简部署指南]] 帮很多人在本地跑起了 OpenClaw。不过毕竟还是本地部署，需要开着电脑才能使用。想要 7x24 咋办呢？答案当然是 Kubernetes。

今天这篇文章就教你用 K8s 把 OpenClaw 部署成真正稳定的、全天候在线的服务。

## 部署 OpenClaw

部署前需要准备两个必需的信息。首先是 Telegram bot token。打开 Telegram 找 @BotFather，发送 `/newbot` 创建一个新的 bot，然后保存好 token：

```bash
export telegramBotToken="<你的-telegram-bot-token>"
```

然后生成一个网关 token，这个是用来访问 OpenClaw Web UI 的：

```bash
export gatewayToken=$(openssl rand -hex 32)
```

现在可以部署了。用 Helm 直接安装我打包好的 Helm chart：

```bash
helm install openclaw oci://ghcr.io/feiskyer/openclaw-kubernetes/openclaw \
  --create-namespace --namespace openclaw \
  --set secrets.openclawGatewayToken=$gatewayToken \
  --set secrets.telegramBotToken=$telegramBotToken
```

这条命令会在 openclaw 命名空间里创建一个 StatefulSet，运行 OpenClaw 的网关服务。等几分钟让 Pod 启动。

验证部署。跑：

```bash
kubectl get pods -n openclaw
```

看到 `openclaw-0` 的 STATUS 是 Running，说明成功了。

然后暴露服务。最简单的方式是端口转发：

```bash
kubectl port-forward -n openclaw openclaw-0 18789:18789
```

打开浏览器访问 <http://localhost:18789/?token=$gatewayToken>，就能进入 OpenClaw 的 Web UI 了。到这里就成功部署了。

如果后面想升级到新版本，用 helm upgrade 命令。想删除的话用 helm uninstall。

## 怎么使用免费的 LLM 模型？

部署成功后，进入 OpenClaw 的 Web UI，或者在容器内运行 onboard 命令重新配置：

```bash
kubectl -n openclaw exec -it openclaw-0 -- node openclaw.mjs onboard
```

选择 QWen 或 OpenCode Zen 作为提供商，OAuth 登录，然后从列表中选择免费模型即可。

## 怎么修改 OpenClaw 的配置？

部署后想改配置的话，也是用 kubectl 命令进入容器修改：

```bash
kubectl -n openclaw exec -it openclaw-0 -- node openclaw.mjs onboard
```

这个命令会以交互式提示让你重新配置 AI 提供商、Telegram bot 连接、Discord 或其他集成等。修改完成后的配置会保存在 PV 中，这样 Pod 重启也不会丢失。

## 怎么授权 Telegram 用户？

OpenClaw 部署成功后默认不允许任何人使用。在 Web UI 里进入 Channel → Telegram，配置 Allow From 来添加允许的用户 ID。你可以给 @userinfobot 发消息来查询自己的 Telegram 用户 ID。

## 怎么加入 Moltbook 社区？

向 OpenClaw 发送以下提示：

```
Read https://moltbook.com/skill.md and follow the instructions to join Moltbook
```

OpenClaw 会引导你完成加入社区的所有步骤。

## 升级和回滚

升级到新版本：

```bash
helm upgrade openclaw oci://ghcr.io/feiskyer/openclaw-kubernetes/openclaw \
  --namespace openclaw \
  --set secrets.openclawGatewayToken=$gatewayToken \
  --set secrets.telegramBotToken=$telegramBotToken
```

照着上面的步骤来就行。如果遇到问题，欢迎到 Github 提 issue，或者提 PR 修复。

---

**相关资源**

- OpenClaw 官网 <https://openclaw.ai/>
- OpenClaw Helm Chart 仓库 <https://github.com/feiskyer/openclaw-kubernetes>
- 前文：[[history/2026-01-30-OpenClaw 极简部署指南.md|OpenClaw 极简部署指南]]
