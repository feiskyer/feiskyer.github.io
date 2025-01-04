---
title: "Notes about serverless"
date: 2016-02-26 21:26:00
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

## Serverless Frameworks

- [Chalice](https://github.com/awslabs/chalice) (AWS Labs): An open source project that provides a Python serverless microframework for AWS that allows you to quickly create and deploy applications that use Amazon API Gateway and AWS Lambda. It makes assumptions about how applications will be deployed, and it has restrictions on how an application can be structured.
- [Claudia.js](https://claudiajs.com/) (Claudia.js): Claudia.js makes it easy to deploy Node.js projects to [AWS Lambda](http://docs.aws.amazon.com/lambda/latest/dg/welcome.html) and [API Gateway](https://aws.amazon.com/api-gateway/). It automates all the error-prone deployment and configuration tasks, and sets everything up the way [JavaScript](http://www.thenewstack.io/tag/JavaScript) developers expect out of the box. Its founder, [Gojko Adzic](https://twitter.com/gojkoadzic), has created extension libraries to let users quickly build chatbots and Web API endpoints.
- [DEEP Framework](https://github.com/MitocGroup/deep-framework) (Mitoc Group): A full-stack JavaScript framework for building cloud-native web applications regardless of specific cloud providers. It is used to support Mitoc’s [DEEP Marketplace](https://www.deep.mg/), which is a software service that lets customers choose and deploy from lists of microservices.
- [Gestalt Framework](http://www.galacticfog.com/product) (Galactic Fog): A set of microservices that are used together create a platform for application developers to build functionality without managing a container environment. The company is a Mesosphere [partner](http://thenewstack.io/galactic-fog-brings-serverless-container-ecosystem/), so may be one of the first ways to execute Lambda functions on Mesosphere’s [Data Center Operating System ](http://thenewstack.io/tag/Data-Center-Operating-System/)(DC/OS).
- [Serverless Framework](http://www.serverless.com/) (Serverless, Inc.):  Serverless is an application framework for building web, mobile and IoT applications exclusively on Amazon Web Services’ Lambda and API Gateway. It’s a command line interface. The company behind it, Serverless, Inc. recently raised over [$3 million in funding](https://techcrunch.com/2016/10/12/serverless-raises-3m-to-help-developers-go-serverless/). The New Stack recently interviewed its creator, [Austen Collins](https://twitter.com/austencollins).  
- [Shep](https://github.com/bustlelabs/shep) (Bustle): Shep is a framework for building JavaScript APIs with AWS API Gateway and Lambda. It was created and used by [Bustle’s](http://thenewstack.io/bustle-migrated-100-million-events-per-day-product-serverless/) engineering team.
- [Sparta](http://gosparta.io/) (Open source project): Sparta offers a Go framework for AWS Lambda microservices. This project is led by NodeSource’s [Matt Weagle](https://twitter.com/mweagle). Sparta lets your Lambda-based service be integrated with the entire set of AWS lambda [event sources](http://docs.aws.amazon.com/lambda/latest/dg/intro-core-components.html). It also can provision [CloudFormation](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) supported resources.
- [Zappa](https://github.com/Miserlou/Zappa) (Open source project): Serverless Python web services that make it easy to deploy Python WSGI applications (i.e., based on frameworks like [Django](https://www.djangoproject.com/) and [Flask](http://flask.pocoo.org/)), on AWS Lambda and API Gateway. A few months ago [Ryan Brown](https://twitter.com/ryan_sb) conducted an interesting [interview](https://serverlesscode.com/post/rich-jones-interview-django-zappa/) with founder [Rich Jones](https://github.com/Miserlou).

## Serverless Platforms

- [Apex](http://apex.run/) (PubNub): Lets you build, deploy, and manage AWS Lambda jobs. [Apex](http://thenewstack.io/apex-makes-aws-lambda-easy-peasy-programmers/) allows the use of non-natively supported language by using a Node.js shim injected into the build. Testing functions and other tooling is also part of the project, which is sponsored by [PubNub](http://thenewstack.io/pubnub-makes-network-programmable/).
- [Funktion](https://github.com/fabric8io/funktion) (Red Hat): An open source, event-driven, lambda-style programming model on top of [Kubernetes](http://kubernetes.io/). A _funktion_ (note the funky spelling) is a regular function written in any language![funktion-redhatproject](https://thenewstack.io/wp-content/uploads/2016/10/Funktion-RedHatproject.png), but then connected to a trigger that is deployed into Kubernetes. When activated, these triggers work with endpoint URLs for databases, messaging systems and many other cloud services. The project is still experimental.
- [Iron.io Platform](https://www.iron.io/platform/) (Iron.io): The platform includes [IronWorker](https://www.iron.io/platform/ironworker/), [IronMQ](https://www.iron.io/platform/ironmq/) and [IronCache](https://www.iron.io/platform/ironcache/), and is[ pre-integrated into many cloud-native platforms](http://thenewstack.io/iron-io-brings-serverless-computing-cloud-foundry-platform/), such as Cloud Foundry, Kubernetes, Mesos and others.With IronWorker you can run [AWS Lamba-like serverless functions](https://www.iron.io/aws-lambda-vs-ironworker/) from inside your firewall. IronWorker is a platform that isolates the code and dependencies of individual tasks to be processed on demand in a containerized environment. IronMQ is a distributed queue service and IronCache is a data service.
- [Gordon](https://github.com/jorgebastida/gordon) (Open source project): Gordon is a platform to create, wire and deploy AWS Lambdas using CloudFormation. [Jorge Bastida](https://twitter.com/jorgebastida) is the leading developer for this project.
- [Nano Lambda](http://nano-lambda.com/) (Nano Lambda): An automated compute service that runs and scales microservices. Code is uploaded into a container. Outside of the container, Nano Lambda will orchestrate the required tasks to network, secure, authenticate and log the micro-service. We learned about this emerging company from an [Adrian Cockcroft](https://twitter.com/adrianco) presentation and look forward to seeing how their attempt to make money in the serverless space.
- [Project Kratos](http://go.iron.io/project-kratos) (Iron.io): Still in beta, Project Kratos will enable enterprises to run AWS Lambda functionality in any cloud provider, as well as on-premise. Iron.io already offers another product, IronWorker, that can run [AWS Lamba-like serverless functions](https://www.iron.io/aws-lambda-vs-ironworker/) that is[ pre-integrated into many cloud-native platforms](http://thenewstack.io/iron-io-brings-serverless-computing-cloud-foundry-platform/).
- [Syncano](https://www.syncano.io/) (Syncano): Syncano is a platform for building serverless apps, allowing users to customize sockets, which are configurations connected to Syncano services. It offers a dashboard and SDKs to define data schema. The company is among the most mature in the serverless space.

## Serverless Tools

- [IOpipe](https://www.iopipe.com/) (IOpipe): IOpipe is analytics and distributed tracing service to monitor Amazon Lambda functions. Users add a module to their Lambda functions to get telemetry. IOpipe aggregates data, sends email reports and will provide a dashboard and metrics. Its founder is [Eric Windisch](https://twitter.com/ewindisch), a Docker alum, was our podcast guest in both in [2014](http://thenewstack.io/the-new-stack-analysts-show-23-docker-its-just-the-beginning/) and [2015](http://thenewstack.io/tns-analysts-show-56-the-pancake-breakfast-circuit-comes-to-containercon/).
- [Kaazing WebSocket Gateway](https://kaazing.com/products/websocket-gateway/editions/) (Kaazing): This network gateway provides a single access point for real-time, web-based protocol elevation that supports load balancing, clustering, and security management. It is available in a free (community) and enterprise edition.
- [Kappa](https://github.com/garnaat/kappa) (Open source project): Kappa is a command line tool that (hopefully) makes it easier to deploy, update, and test functions for AWS Lambda.
- [LambCI](http://lambci.org/) (Open source project): LambCI is a continuous integration system built on AWS Lambda. It is a package you can upload to AWS Lambda that gets triggered when you push new code or open pull requests on GitHub and runs your tests in the Lambda environment itself. While founder [Michael Hart](https://twitter.com/hichaelmart) launched LambCI with a [compelling case](https://medium.com/@hichaelmart/lambci-4c3e29d6599b#.pdaqdnq4a) to use it, there may not yet be a market for it as a commercial offering.
![Assumes 7 days/wk — with LambCI running on fastest 1.5GB Lambda option)](https://thenewstack.io/wp-content/uploads/2016/10/1-lBa176N3CqOl2su9iTyCAw.png)
-  [Pusher](https://pusher.com/) (Pusher): Pusher is a hosted real-time messaging service with APIs, developer tools and open source libraries that simplify integrating real-time functionality into web and mobile applications.
- [Vandium-node](https://github.com/vandium-io/vandium-node) (Vandium Software): An AWS Lambda wrapper, Vandium is an open source npm module for protecting Node.js security using validation and protecting against injection attacks. This project and its eponymous [company](https://vandium.io/) appear to be led by [Richard Hyatt](https://github.com/richardhyatt), a co-founder of [BlueCat Networks](https://www.bluecatnetworks.com/).
- [Webtask](https://webtask.io/) (Auth0): Webtask [uses HTTP calls](http://thenewstack.io/often-choose-webtask-lambda/) to run server-side code for your JavaScript and native applications. Auth0’s [primary offering](https://auth0.com/how-it-works) is a set of authentication services for mobile and serverless applications.


## Miscellaneous Serverless Resources

- [Dexter](http://rundexter.com/): Dexter is a platform that to connect third-party APIs. The development team is focusing on the “bot” use cases.
- [Flourish](http://thenewstack.io/amazon-debuts-flourish-runtime-application-model-serverless-computing/) (AWS): As we reported earlier in the year, Flourish will be an open source platform to manage components of serverless applications. Although it has not been released yet, Flourish gets a lot of mindshare among serverless developers.
- [Form.io](https://form.io/) (Form.io): A combined form and API platform for [Angular](http://www.thenewstack.io/angular) and [React](http://www.thenewstack.io/tag/React), Form.io simplifies connections between your forms and APIs.
- [nstack](http://nstack.com/) (nstack): The nstack software turns a piece of code (such as a function, a class, or a library) into a lightweight microservice that can be bound to a stream of events. It used to be called Stackhut.
- [Serverless Calculator](http://serverlesscalc.com/) (Serverless, Inc.): This calculator helps compare estimated costs across different FaaS providers, initially for AWS Lambda and Azure Functions. When Google Cloud Functions and IBM OpenWhisk set their pricing, this information will be included also.
[![](https://thenewstack.io/wp-content/uploads/2016/10/serverlesscalc.png)](http://serverlesscalc.com/)
- [Stamplay](https://stamplay.com/) (Stamplay): Stamplay connects APIs into service-based applications.

## **Serverless Consultancies**

_In so many emerging technology spaces, most companies are comprised mostly of manpower, implementing projects, not selling intellectual property. These companies are just a few examples._ 

- [Cloudonaut](https://cloudonaut.io/serverless-consulting/)
- [Microapps](http://microapps.com/serverless-consulting/)
- [Serverless Heroes](https://serverlessheroes.com/)
- [SGA Serverless](http://sga.com/)
- [Trek10](https://www.trek10.com/)
- [Useful IO](http://www.useful.io/)



**参考**

[1] [AWS Lambda  introduction ](http://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
[2] [OpenStack和Docker不能，Kubernetes和Mesos也不能，ServerLess能决定云计算胜负吗](http://mp.weixin.qq.com/s?__biz=MzAxODUwNDE1Mg==&mid=407457372&idx=1&sn=5666314daaf7a3f4f224eaa6b31f7c30&3rd=MzA3MDU4NTYzMw==&scene=6#rd)
[3] [Google Cloud Functions](https://cloud.google.com/functions/docs)
[4] [Google引入云函数（Cloud Functions）服务](http://www.infoq.com/cn/news/2016/02/google-cloud-functions)
[5] <http://thenewstack.io/tns-guide-serverless-technologies-best-frameworks-platforms-tools/>

