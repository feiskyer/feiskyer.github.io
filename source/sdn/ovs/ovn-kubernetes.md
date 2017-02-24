# OVN Kubernetes

* https://github.com/openvswitch/ovn-kubernetes


There is active development on a [CNI plugin for OVN to be used with Kubernetes](https://github.com/openvswitch/ovn-kubernetes).  One of the key goals for OVN was to have containers in mind from the beginning, and not just VMs.  Some important features were added to OVN to help support this integration.  For example, ovn-kubernetes makes use of OVN’s load balancing support, which is built on native load balancing support in OVS.

The README in that repository contains an overview, as well as instructions on how to use it.  There is also support for [running an ovn-kubernetes environment using vagrant](https://github.com/openvswitch/ovn-kubernetes/tree/master/vagrant).



