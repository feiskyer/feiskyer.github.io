---
title: Serverless开源框架
layout: "post"
---

常见的Serverless开源框架简介。

## 基于Kuberetes的Serverless框架

- [Fission](https://github.com/platform9/fission)
- [Funktion](https://github.com/fabric8io/funktion): 通过fabric8-maven-plugin生成镜像和Manifests，同时兼容Kubernetes和Openshift
- [Kubeless](https://github.com/skippbox/kubeless): 基于ThirdPartyResource和Kafka，目前是POC阶段

## IBM OpenWhisk

OpenWhisk是IBM发布的开源事件驱动计算平台，剑指AWS Lambda，其代码开源在Github上<https://github.com/openwhisk/openwhisk>。

![arch](OpenWhisk.png)

![flow](OpenWhisk_flow.png)

## 其他Serverless框架

* [Serverless Framework](http://www.serverless.com) - Build and maintain web, mobile and IoT applications running on AWS Lambda and API Gateway (formerly known as JAWS).
* [Apex](http://apex.run) - Minimal AWS Lambda function manager with Go support.
* [Zappa](https://github.com/Miserlou/Zappa) - Serverless Python WSGI with AWS Lambda + API Gateway.
* [ClaudiaJS](https://github.com/claudiajs/claudia) - Deploy Node.js microservices to AWS easily.
* [Lambada Framework](https://github.com/lambadaframework/lambadaframework) - JAX-RS implementation for AWS Lambda.
* [DEEP](https://github.com/MitocGroup/deep-framework) - Full-stack Web Framework for Cloud-Native Applications and Platforms using Microservices Architecture.
* [Turtle](https://github.com/iopipe/turtle/) - library for building functional and actor-driven NodeJS apps on Lambda
* [Sparta](http://gosparta.io) - A framework that transforms a Go application into an AWS Lambda powered microservice.
* [Kappa](https://github.com/garnaat/kappa) - a command line tool that (hopefully) makes it easier to deploy, update, and test functions for AWS Lambda.
* [Shep](https://github.com/bustlelabs/shep) - A framework for building APIs using AWS API Gateway and Lambda
* [python-λ](https://github.com/nficano/python-lambda) - A toolkit for developing and deploying serverless Python code in AWS Lambda
* [λambdify](http://zhukovalexander.github.io/lambdify) - AWS Lambda automation and integration for Python
* [Gordon](https://github.com/jorgebastida/gordon) - λ Gordon is a tool to create, wire and deploy AWS Lambdas using CloudFormation
* [Chalice](https://github.com/awslabs/chalice) - Python serverless microframework from Amazon for AWS lambda
* [Gestalt Framework](http://www.galacticfog.com/product) - Gestalt's Lambda Application SERver (LASER)” for short, is a lambda service that supports running .Net, Javascript, Java, Scala, Ruby, and Python lambdas.
* [lambdoku](https://github.com/kubek2k/lambdoku) - Heroku-like experience when using AWS Lambda
* [IronFunctions](https://github.com/iron-io/functions) - The Serverless Microservices platform
* [PyWren](https://github.com/ericmjonas/pywren) - provides the ability to parse out Python-based scientific workloads across many different Lambda services

