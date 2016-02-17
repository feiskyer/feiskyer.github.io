---
layout: post
title: "Going Native with OpenStack Centric Applications: Murano"
description: ""
category: 
tags: [OpenStack]
---

Following on our previous discussion surveying the projects supporting applications within OpenStack, let’s continue our review with an in-depth look at the OpenStack-native Application Catalog: Murano, currently an incubation status project, having seen its functionality and core services integration advanced over the past few OpenStack releases.

### What is it?

An application catalog developed by Mirantis, HP and others (now including Cisco), that allows application developers and cloud administrators to publish applications in a categorized catalog to be perused and deployed by application consumers. The selection of applications available within the catalog is intended to be that of released versions (ready-state) of applications (cloud-native or enterprise-architected), not application versions that are mid-development. Ideally, these are applications ready to be consumed and run by application users.

### Functionality Highlights

![ui](http://blog.gingergeek.com/wp-content/uploads/2014/11/OpenStack-Centric-Applications-Murano-Application-Catalog-UI.png)

1.  Supports Windows and Linux applications
2.  Leverages HOT templates for application definition
3.  Controls Heat stack creation and updates processes
4.  Track application properties and dependencies
5.  Defines provisioning workflow definitions and executes them
6.  Introduces “Application” and “Environment” constructs
7.  Provides UI for application topology visualization
8.  Control lifecycle of a deployed application
9.  Allows simple management of access to an application
10.  Compose an environment from multiple application components
11.  Out of the Box Cataloged Applications
    * 16 sample applications available now
    * 6 production-grade applications の Mirantis OpenStack Express**
12.  Multiple application formats supported:
    * HOT Templates
    * MuranoPL
13.  Vision to support
    * Other application model formats:
    * Parallels APS format
    * TOSCA format
    * Pricing; billing system integration

### User Personas & Capabilities

As an application catalog, Murano, primarily focuses on three user personas, the Cloud Administrator, Application Consumer and Application Publisher receiving the most emphasis upfront in the development of this project.

### Application Consumer

The Application Consumer selects and deploys instances of applications into environments they define. The Application Consumer also* 

* browses catalog (search, category, tags, etc)
* creates new environments
* deploys applications in environments
* monitors application statistics

### Application Publisher

The Application Publisher creates application definitions (packages) that are imported as entries into the application catalog for perusal by Application Consumers. The Application Publisher also* 

* defines application metadata (author, help message, version, etc)
* identifies cloud resource allocation (HOT templates)
* creates application deployment specifications (HOT templates)
* defines a template for dynamic visualization of application topology (Horizon)
* identifies metrics collection (Ceilometer)
* establishes actions and events (Murano and Mistral)
* imports and publishes application definition to catalog

### Cloud Administrator

The Cloud Administrator is responsible for running the application catalog and providing stable infrastructure upon which to deploy and run applications. The Cloud Administrator also* 

* curates application catalog (certification and signing of packages)
* configures access to applications
* defines billing rules*

### Application Packaging Process

Currently, Murano applications may be packaged using two different formats to describe the application – the MuranoPL or a HOT template. There’s roadmap to support addition application description formats. While these two methodologies vary in terms of how the orchestration is performed during provisioning of an instance of the app, their are common attributes (catalog metadata) like an application display name, logo, description, author, tags. For those familiar with other domain-specific languages of other popular configuration management frameworks, the MuranoPL is of little challenge to pick up (you may lean into  use Bash or Powershell if more comfortable) or you may opt to use SoftwareConfig and SoftwareDeploy of HOT.

![](/assets/OpenStack-Centric-Applications-Murano-Application-Packaging.png)

### Architectural Overview & Core Services Integration

See the “Murano Architectural Overview” diagram for a visual representation of how Murano is tightly integrated with core OpenStack services. It’s relationship to existing core services breaks down as follows:

<img src="/assets/OpenStack-Centric-Applications-Murano-Architectural-Overview.png" alt="Overview" width="800px" />

* Glance: Originally designed as an image repository, Murano will use Glance to store & query application definitions. Glance is used as an artifact repository to store application definitions, query & search them and store images required by applications. Images used by Murano are marked with specific metadata, which is used by Murano to derive appropriate selections within the UI during application deployment time.
* Heat: Cloud resource allocation specific to the application, Resources required by application is allocated using Heat, Application provisioning / deployment via Heat Software Configuration, Life-cycle callbacks
* Horizon: Horizon is used to provide the Application Catalog user interface wherein Application Publishers may browse and deploy applications. Horizon is also used to both build applications and visualize the topology provisioned applications. The need for this type of dynamic user interface (application topology canvas) has been proposed as separate project to provide common support to other Application-oriented projects – Heat, Solum, Mistral and Murano. This application blueprint designer project is codename – Merlin.
* Docker: Murano supports existing Nova and Heat plugins. 
* Ceilometer: Murano uses Ceilometer for application metric collection & processing. Additionally, Ceilometer events may be subscribed to and trigger specific actions (see below) for autoscaling, HA, DR and other.
* Workflows are used when complex workflow outside of Heat is needed.
* Actions: Application level ad-hoc actions (e.g. create backup, enable/disable some feature, or create user for an application) will also be defined in Mistral. Classic runbook automation applies here – Murano allows the Application Publisher to define various custom actions to be taken upon trigger by an interesting event. What constitutes and interesting event is up to the Application Publisher, who may define any action in the application definition and associate the action to a specific workflow. By exposing a webhook to trigger the action (and workflow), they may be triggered by Ceilometer alarms or any 3rd party tool. Common use cases are auto-scaling, HA and DR. The “Murano Actions” diagram shows an example of an autoscaling scenario in which an application might require additional database instance based web server load.

<img src="/assets/OpenStack-Centric-Applications-Murano-Actions.png" alt="Drawing" width="800px" />

### Murano and Containers

Murano inherently supports Docker containers by relying upon existing OpenStack components for container integration and orchestration. This means that there are no considerations to be accounted for within the MuranoPL to describe the application package to support containers. Similarly, when using Heat templates at the core of the application package, only&nbsp;reference to Docker resources and images is needed to support container orchestration by Heat. There are different ways of using Docker in OpenStack via Murano:

1) Heat template can use Heat::Docker

* <span style="line-height: 1em;">Heat::Docker driver leverages Heat engine directly to instantiate containers</span>
* <span style="line-height: 1em;">Use Heat when Nova does not support Docker</span>

2) Heat template can use Nova::Docker

 * <span style="line-height: 1em;">Use when you have a bare metal Docker installation</span>
 * <span style="line-height: 1em;">Through Nova API, create a container without a VM being created to host</span>
 * <span style="line-height: 1em;">Nova can go to bare metale to create Docker container</span>
 * <span style="line-height: 1em;">User provides Heat template, workflow (Murano DSL) and image</span>

 3) Not recommended – Use Heat resource to create a VM with Dockerénside and boot an image file to the VM with `docker run`.

* The Murano team is looking to add autoscaling for Docker services, facilitate Docker application placement and integration with monitoring and network services.

### Murano as a Southbound Catalog

Murano has two different northbound APIs to expose access to applications in the catalog – REST and AMQP (Services Broker). Within the Juno release, the Services Broker has only been prototyped. It’s scheduled to be fully-implemented in Kilo. While other use cases may exist, the primary use case for these northbound API revolves around allowing northbound catalogs to access and expose OpenStack-native applications.

The Services Broker supports CRUD and binds service with your application. A proof of concept has been completed to integrate Cloud Foundry with Murano via the Service Broker. When CloudFoundry is integrated to Murano, CloudFoundry users see and order Murano applications in CloudFoundry.

Using the REST API, Murano may be integrated as a southbound application catalog to expose OpenStack-native applications as SaaS application profiles available for users of a northbound catalog. Users benefit from existing services offered on top of OpenStack. This enables application components to be split across infrastructure (having application components deployed into different infrastructures).

### Kilo Roadmap

While subject to change, based on Kilo design summit discussions this week, the project team aims to bite off the following capabilities before the next release in May.

* Implementing CloudFoundry ServiceBroker API
* Use of Glance as an artifact repository
* Support pluggable package definitions formats:

    * TOSCA (Topology and Orchestration Specification for Cloud Applications)
    * APS (Parallels Application Standard)

* Multiple Heat Stacks and OpenStack Cloud support

    * Availability Zones (for DR)
    * Multiple OpenStack clouds

* Pluggable Architecture

    * Integration with 3rd party API (F5, Brocade etc.)
    * Package format plugins

From <http://blog.gingergeek.com/2014/11/going-native-with-openstack-centric-applications-murano/>
