---
title: sysdig
date: 2016-10-21 17:26:05
---

# Tips of sysdig

Sysdig captures system calls and other system level events using a linux kernel facility called tracepoints, providing a rich set of real-time, system-level information.

Sysdig "packetizes" this information, so that you can do things like save it into trace files and easily filter it, a bit like you would do with tcpdump. This makes it very flexible to explore what processes are doing.

Sysdig instruments your physical and virtual machines at the OS level by installing into the Linux kernel and capturing system calls and other OS events. Then, using sysdig's command line interface, you can filter and decode these events in order to extract useful information. Sysdig can be used to inspect systems live in real-time, or to generate trace files that can be analyzed at a later stage.

- User Guide: <https://github.com/draios/sysdig/wiki/Sysdig%20User%20Guide>
- Source code: <https://github.com/draios/sysdig>

## Install

```sh
# brew install sysdig
curl -s https://s3.amazonaws.com/download.draios.com/stable/install-sysdig | sudo bash
sysdig-probe-loader
```

##  Networking

* See the top processes in terms of network bandwidth usage
> sysdig -c topprocs_net

* Show the network data exchanged with the host 192.168.0.1
> as binary:
> sysdig -s2000 -X -c echo_fds fd.cip=192.168.0.1
as ASCII:
> sysdig -s2000 -A -c echo_fds fd.cip=192.168.0.1

* See the top local server ports
> in terms of established connections:
> sysdig -c fdcount_by fd.sport "evt.type=accept"
> in terms of total bytes:
> sysdig -c fdbytes_by fd.sport

* See the top client IPs
> in terms of established connections
> sysdig -c fdcount_by fd.cip "evt.type=accept"
> in terms of total bytes
> sysdig -c fdbytes_by fd.cip

* List all the incoming connections that are not served by apache.
> sysdig -p"%proc.name %fd.name" "evt.type=accept and proc.name!=httpd"

## Containers

* View the CPU usage of the processes running inside the wordpress1 container
> sudo sysdig -pc -c topprocs_cpu container.name=wordpress1

* View the network bandwidth usage of the processes running inside the wordpress1 container
> sudo sysdig -pc -c topprocs_net container.name=wordpress1

* View the processes using most network bandwidth inside the wordpress1 container
> sudo sysdig -pc -c topprocs_net container.name=wordpress1

* View the top files in terms of I/O bytes inside the wordpress1 container
> sudo sysdig -pc -c topfiles_bytes container.name=wordpress1

* View the top network connections inside the wordpress1 container
> sudo sysdig -pc -c topconns container.name=wordpress1

* Show all the interactive commands executed inside the wordpress1 container
> sudo sysdig -pc -c spy_users container.name=wordpress1

## Application

* See all the GET HTTP requests made by the machine
> sudo sysdig -s 2000 -A -c echo_fds fd.port=80 and evt.buffer contains GET

* See all the SQL select queries made by the machine
> sudo sysdig -s 2000 -A -c echo_fds evt.buffer contains SELECT

* See queries made via apache to an external MySQL server happening in real time
> sysdig -s 2000 -A -c echo_fds fd.sip=192.168.30.5 and proc.name=apache2 and evt.buffer contains SELECT

## Disk I/O

* See the top processes in terms of disk bandwidth usage
> sysdig -c topprocs_file

* List the processes that are using a high number of files
> sysdig -c fdcount_by proc.name "fd.type=file"

* See the top files in terms of read+write bytes
> sysdig -c topfiles_bytes

* Print the top files that apache has been reading from or writing to
> sysdig -c topfiles_bytes proc.name=httpd

* Basic opensnoop: snoop file opens as they occur
> sysdig -p "%12user.name %6proc.pid %12proc.name %3fd.num %fd.typechar %fd.name" evt.type=open

* See the top directories in terms of R+W disk activity
> sysdig -c fdbytes_by fd.directory "fd.type=file"

* See the top files in terms of R+W disk activity in the /tmp directory
> sysdig -c fdbytes_by fd.filename "fd.directory=/tmp/"

* Observe the I/O activity on all the files named 'passwd'
> sysdig -A -c echo_fds "fd.filename=passwd"

* Display I/O activity by FD type
> sysdig -c fdbytes_by fd.type

## Processes and CPU usage

* See the top processes in terms of CPU usage
> sysdig -c topprocs_cpu

* See the top processes for CPU 0
> sysdig -c topprocs_cpu evt.cpu=0

* Observe the standard output of a process
> sysdig -s4096 -A -c stdout proc.name=cat

## Performance and Errors

* See the files where most time has been spent
> sysdig -c topfiles_time

* See the files where apache spent most time
> sysdig -c topfiles_time proc.name=httpd

* See the top processes in terms of I/O errors
> sysdig -c topprocs_errors

* See the top files in terms of I/O errors
> sysdig -c topfiles_errors

* See all the failed disk I/O calls
> sysdig fd.type=file and evt.failed=true

* See all the failed file opens by httpd
> sysdig "proc.name=httpd and evt.type=open and evt.failed=true"

* See the system calls where most time has been spent
> sysdig -c topscalls_time

* See the top system calls returning errors
> sysdig -c topscalls "evt.failed=true"

* snoop failed file opens as they occur
> sysdig -p "%12user.name %6proc.pid %12proc.name %3fd.num %fd.typechar %fd.name" evt.type=open and evt.failed=true

* Print the file I/O calls that have a latency greater than 1ms:
> sysdig -c fileslower 1

## Security

* Show the directories that the user "root" visits
> sysdig -p"%evt.arg.path" "evt.type=chdir and user.name=root"

* Observe ssh activity
> sysdig -A -c echo_fds fd.name=/dev/ptmx and proc.name=sshd

* Show every file open that happens in /etc
> sysdig evt.type=open and fd.name contains /etc

* Show the ID of all the login shells that have launched the "tar" command
> sysdig -r file.scap -c list_login_shells tar

* Show all the commands executed by the login shell with the given ID
> sysdig -r trace.scap.gz -c spy_users proc.loginshellid=5459

* Applied use of sysdig for forensics analysis:
  * [Fishing for Hackers: Analysis of a Linux Server Attack](http://draios.com/fishing-for-hackers/)
  * [Fishing for Hackers (Part 2): Quickly Identify Suspicious Activity With Sysdig](http://draios.com/fishing-for-hackers-part-2/)

