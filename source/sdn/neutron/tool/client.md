# Python neutron client

## Keystone client

```python
# pip install keystoneauth
def keystone_client():
    import os
    from keystoneauth1 import identity
    from keystoneauth1 import session
     from keystoneclient.v2_0 import client
    kwargs = {"auth_url": os.getenv("OS_AUTH_URL"),
              "username": os.getenv("OS_USERNAME"),
              "password": os.getenv("OS_PASSWORD"),
              "project_name": os.getenv("OS_TENANT_NAME"),
              }
    auth = identity.Password(**kwargs)
    sess = session.Session(auth=auth)
    keystone = client.Client(session=sess)
    return keystone
```

## Neutron client

```python
def neutron_client():
    import os
    from keystoneauth1 import identity
    from keystoneauth1 import session
    from neutronclient.v2_0 import client
    kwargs = {"auth_url": os.getenv("OS_AUTH_URL"),
              "username": os.getenv("OS_USERNAME"),
              "password": os.getenv("OS_PASSWORD"),
              "project_name": os.getenv("OS_TENANT_NAME"),
              }
    auth = identity.Password(**kwargs)
    sess = session.Session(auth=auth)
    neutron = client.Client(session=sess,
        region_name=os.getenv("OS_REGION_NAME"))
    return neutron
```
