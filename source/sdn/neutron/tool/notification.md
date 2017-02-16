---
title: "监听notification消息"
layout: "post"
---

## 监听notification消息

```python
#!/usr/bin/env python
# coding: utf-8
import logging
import socket
import time
import eventlet
import oslo_messaging
from oslo_config import cfg


# global config
rabbit_username = 'guest'
rabbit_password = 'guest'
hostname = socket.gethostname()
rabbit_hosts = ['127.0.0.1']

eventlet.monkey_patch()
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)


def rabbitmq_listener():
    transports = []
    for host in rabbit_hosts:
        transports.append(oslo_messaging.TransportHost(
            host, 5672, rabbit_username, rabbit_password))
    transport_url = oslo_messaging.TransportURL(
        cfg.CONF, 'rabbit', '/', transports)
    transport = oslo_messaging.get_transport(
        cfg.CONF, transport_url)
    targets = [oslo_messaging.Target(
        topic='notifications', exchange='neutron')]
    endpoints = [NotificationEndpoint()]
    return oslo_messaging.get_notification_listener(
        transport, targets, endpoints,
        allow_requeue=True,
        executor='eventlet',
        pool='test-rmq' + hostname)


class NotificationEndpoint(object):
    filter_rule = oslo_messaging.NotificationFilter(
        publisher_id='^network.*')

    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        log.info("Got event %s from %s with payload: %s" % (
            event_type, publisher_id, payload
        ))

    def warn(self, ctxt, publisher_id, event_type, payload, metadata):
        None

    def error(self, ctxt, publisher_id, event_type, payload, metadata):
        None


if __name__ == "__main__":
    try:
        server = rabbitmq_listener()
        server.start()
        print "Server started"
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "Stopping executor service..."
        server.stop()
        server.wait()
```

## 删除queue

```python
import pika

queue_name = "test"
try:
  connection = pika.BlockingConnection(pika.ConnectionParameters(
                 'localhost'))
  channel = connection.channel()
  channel.queue_delete(queue=queue_name)
finally:
  connection.close()
```

