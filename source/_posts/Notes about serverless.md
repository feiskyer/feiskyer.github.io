layout: "post"
title: "Notes about serverless"
date: "2016-02-26 13:36"
category: cluster
---

“只需要关注数据和业务逻辑，无需维护服务器，也不需要关心系统的容量和扩容”， serverless将大家从server中解放了出来，只需要关注业务逻辑本身。serverless的概念跟PaaS很像，又比传统的PaaS有着更好的易用性。

(未完待续)

## serverless的主要玩家

#### AWS Lambda

AWS Lambda是目前最有影响力的serverless产品，它依据事件响应触发用户自定义的Lambda函数，并自动管理后端的服务器、高可用以及自动扩展等：

> 通过 AWS Lambda，无需配置或管理服务器即可运行代码。您只需按消耗的计算时间付费 – 代码未运行时不产生费用。借助 Lambda，您几乎可以为任何类型的应用程序或后端服务运行代码，而且全部无需管理。只需上传您的代码，Lambda 会处理运行和扩展高可用性代码所需的一切工作。您可以将您的代码设置为自动从其他 AWS 服务触发，或者直接从任何 Web 或移动应用程序调用。

> AWS Lambda是一项计算服务，依响应事件来运行您的代码并为您自动管理底层计算资源。您可以使用 AWS Lambda 通过自定义逻辑来扩展其他 AWS 服务，或创建您自己的按 AWS 规模、性能和安全性运行的后端服务。AWS Lambda 可以自动运行代码以响应多个事件，例如 Amazon S3 存储桶中对象的修改或 Amazon DynamoDB 中的表更新。
>
> Lambda 在可用性高的计算基础设施上运行您的代码，执行计算资源的所有管理工作，其中包括服务器和操作系统维护、容量预配置和自动扩展、代码和安全补丁部署以及代码监控和记录。您只需要提供代码。

其主要特性包括：

- 用自定义逻辑扩展其他 AWS 服务
- 构建自定义后端服务
- 完全自动化的管理，无需关注底层操作系统
- 内置容错能力， 可在各区域中跨过多个可用区维护计算容量
- 自动扩展
- 集成化安全模型
- 自备代码
- 灵活的资源模型
- 目前支持Java、JS、Python等语言
- *Lamdba的价格非常便宜*

Lambda推荐的应用场景包括

- 数据处理，比如文件处理、实时数据流处理或者提取、转换、加载等
- 构建后端以处理 Web、移动、物联网 (IoT) 和第 3 方 API 请求

#### Google Cloud Functions

Google Cloud Functions允许用户创建js函数来自动响应事件，支持发布/订阅模型。用户可以配置一个“触发器”来监听这些事件，通过在Node.js环境执行JavaScript代码对这些事件做出响应。目前，“触发器”可以通过以下途径激活。

- 云发布/订阅（Cloud Pub/Sub）：任何异步的发布/订阅事件
- 云存储（Cloud Storage）：对象变更通知
- HTTP调用：通过HTTP进行的同步调用
- 调试/直接调用：使用命令行界面（CLI）开发/调试“云函数”

Google Cloud Functions还在Alpha阶段，不受SLA限制，因此还不适合用在生产环境。

#### Azure Data Lake

Azure Data Lake提供了针对数据处理场景的ServerLess服务：

> Azure Data Lake 包括了所有所需的功能，使开发人员、数据专家和分析师可以更轻松地存储任何大小、形状和速度的数据以及跨平台和语言进行各种类型的处理和分析。它消除了插入和存储所有数据的复杂性，同时启动更快，可与批量、流式、交互式分析一起运行。Azure Data Lake 与现有 IT 投资一起工作以进行简化数据管理和监管的识别、管理和安全防护工作。同时与操作存储区和数据仓库无缝集成，以便可以扩展当前数据应用程序。我们已充分利用与企业客户合作以及运行 Microsoft 业务（如 Office 365、Xbox Live、Azure、Windows、Bing 和 Skype）一些全球规模最大的处理和分析的经验。Azure Data Lake 使用一种已准备好满足你当前和未来业务需求的服务，解决了许多工作效率和可缩放性的挑战，而正是这些挑战阻止你最大化自己的数据资产价值。

更多产品介绍见 https://azure.microsoft.com/zh-cn/solutions/data-lake

#### IBM OpenWhisk

OpenWhisk是IBM发布的开源事件驱动计算平台，剑指AWS Lambda，其代码开源在Github上https://github.com/openwhisk/openwhisk。

![arch](https://github.com/openwhisk/openwhisk/raw/master/docs/OpenWhisk.png)

#### Facebook Parse

Parse是专为移动应用提供后台服务的云计算平台，Parse为开发者承接了繁琐的后台服务，让开发者只需专注于具体的前端开发工作。它提供任意数据存储、通知发送/推送、地理位置数据使用、Facebook/Twitter 登陆帐号添加等服务。

Facebook在2013年将其收购，并于今年一月份宣布关闭Parse服务并将其开源，开源地址在https://github.com/ParsePlatform/parse-server。

参考

[1] [AWS Lambda  introduction ](http://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
[2] [OpenStack和Docker不能，Kubernetes和Mesos也不能，ServerLess能决定云计算胜负吗](http://mp.weixin.qq.com/s?__biz=MzAxODUwNDE1Mg==&mid=407457372&idx=1&sn=5666314daaf7a3f4f224eaa6b31f7c30&3rd=MzA3MDU4NTYzMw==&scene=6#rd)
[3] [Google Cloud Functions](https://cloud.google.com/functions/docs)
[4] [Google引入云函数（Cloud Functions）服务](http://www.infoq.com/cn/news/2016/02/google-cloud-functions)
