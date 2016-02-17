---
layout: post
title: "Going Native with OpenStack Centric Applications: Overview"
description: ""
category:
tags: [OpenStack]
---

Cloud infrastructure is useless without applications running atop, providing business services and&nbsp;solving customer needs. So, as applications ascend to the throne as the rightful king of cloud, focus sharpens on their support within OpenStack-based clouds.&nbsp;With this focus, let’s walk through a survey of components and projects supporting applications in OpenStack, understanding what a&nbsp;day in the life of an application in OpenStack is like. We’ll start with an overview of the application ecosystem comprised of a number of supporting projects. In the ecosystem overview below, relevant OpenStack projects are presented in context of existing, similar technologies with which you may be familiar. These similar technologies both under and overlap functionality of the respective OpenStack project, but are shown to hasten your general&nbsp;understanding of which bucket these projects fall into by way of tech you may already know (so, add a pinch of salt when considering relevancy of suggested affiliated technologies).


### Application Ecosystem by Project

Like individual lines in a product family, projects within OpenStack engulf and extend one another for related, but distinct purposes and target use cases. OpenStack developers are cautious to apply DRY principles in their approach to project design, integrating functionality rather than reinventing the wheel as they go. The _Project Focus and Relationship_ diagram both figuratively and literally places project relationships into round bubbles, identifying conceptual starting points for the genesis of an application as well as the reuse of some projects by others.

![](/assets/OpenStack-Centric-Applications-Project-Focus-and-Relationship.png)

* **Application Blueprint Designer –&nbsp;[Merlin](https://wiki.openstack.org/wiki/Merlin)**

    * RavelloSystems, UrbanCode, CliQr, Prime Service Catalog*…

* **Application Lifecycle Management PaaS – [Solum](https://wiki.openstack.org/wiki/Solum)**

    * Similar technologies (ALM) – Atlassian Suite, HP ALM, Cloudpipes, Serena…
    * Similar technologies (PaaS) – Openshift, Cloud Foundry, BlueMix, AppScale, Heroku, App Engine…

* **Application Catalog –&nbsp;[Murano](https://wiki.openstack.org/wiki/Murano)**

    * Similar technologies – AppStack, CliQr, ITApp, AppDirect…

* **Application Stack Provisioning – [Heat](https://wiki.openstack.org/wiki/Heat),&nbsp;Magnum**

    * Similar technologies – AWS Elastic Beanstalk, Kubernetes, GearD, Warden, Fleet, MaestroNG, CliQr, Nirmata…

* **Application Containers –&nbsp;[Docker](https://wiki.openstack.org/wiki/Docker)**

    * Similar technologies – OpenVZ, Linux V-Server, FreeBSD jails,&nbsp;AIX&nbsp;Workload Partitions&nbsp;and&nbsp;Solaris Containers

* **Application Configuration Management – Puppet, Chef**

    * Similar technologies – Heat, Salt, Ansible, [Satori](https://wiki.openstack.org/wiki/Satori)\*…

### A Day in the Life of an OpenStack-Native Application

The _Application Lifecycle Flows_ diagram defines different&nbsp;entrance points by which applications are birthed and the flow between different OpenStack projects within their lifecycle.

![](/assets/OpenStack-Centric-Applications-Application-Lifecycle-Flows.png)

Users may&nbsp;**design** applications with Merlin,&nbsp;**develop**&nbsp;applications with Solum,&nbsp;**order** applications with Murano,&nbsp;**deploy** applications and resources with Heat and&nbsp;**manage** applications with Puppet/other configuration managers.

### “Applications”

Given that applications are varied in nature both in terms of their type and complexity, let’s take a moment to review their possible shapes and sizes. With regard to types of applications, some are &nbsp;image-based and some are container-based while others are offered simply as a&nbsp;SaaS subscription (implying that a singular instance of this application may serve multiple tenants). Applications may be cloud-native (designed to be scaled out, highly distributed, service-oriented) or enterprise-architected (designed to be scaled up, designed with layers and functional domains). Application complexity ranges from single component (image or container) to multiple component, multiple environment, multiple OpenStack deployments to OpenStack and other systems. Applications may be comprised of multiple components (e.g. MySQL, PHP, Apache) or a singular components (MySQL). Application components may be distributed or contained within a given container, VM or cloud. With these possibilities in mind,&nbsp;let’s begin our survey of their support with the&nbsp;OpenStack-native application catalog – Murano in the next post in this series.

From <http://blog.gingergeek.com/2014/11/going-native-with-openstack-centric-applications-overview/>
