---
layout: post
title: "How to disable ubuntu services"
description: ""
category: Linux
tags: [Linux, ubuntu]
---

To toggle a service from starting or stopping permanently you would need to:

    echo manual | sudo tee /etc/init/SERVICE.override

where the stanza manual will stop Upstart from automatically loading the service on next boot. Any service with the .override ending will take precedence over the original service file. You will only be able to start the service manually afterwards. If you do not want this then simply delete the .override. For example:

    echo manual | sudo tee /etc/init/mysql.override

Will put the MySQL service into manual mode. If you do not want this, afterwards you can simply do

    sudo rm /etc/init/mysql.override

and Reboot for the service to start automatically again. Of course to enable a service, the most common way is by installing it. If you install Apache, Nginx, MySQL or others, they automatically start upon finishing installation and will start every time the computer boots. Disabling as mentioned above will make state of the service manual.
