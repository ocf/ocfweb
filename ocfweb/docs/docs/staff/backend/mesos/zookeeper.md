[[!meta title="Zookeeper"]]

Zookeeper is a distributed key-value store. It has strong durability and
consistency guarantees, and reasonably high availability. Like Mesos, it
requires a quorum of masters to be available for a leader to be elected. No
work can be done without a leader.

Zookeeper runs on each of the Mesos masters, though in principle it could run
anywhere. It's a core dependency of all Mesos-related infrastructure at the
OCF.


## General troubleshooting steps
### How do I find whether this node is a leader or follower?

```
$ echo srvr | nc localhost 2181
Zookeeper version: 3.4.5--1, built on 10/01/2016 18:09 GMT
Latency min/avg/max: 0/5/58
Received: 31
Sent: 30
Connections: 1
Outstanding: 0
Zxid: 0x2800000136
Mode: follower
Node count: 790
```

(You can replace `localhost` with `mesos#` to try different servers remotely.)


### How do I use the Zookeeper CLI?

Zookeeper has a CLI from which you can inspect the data in Zookeeper. To use
it, SSH to any of the Mesos masters and run the command `sudo
/usr/share/zookeeper/bin/zkCli.sh`. (This command must be run as root because it reads the password from a file only readable by root.)

You'll be given a prompt. Here are some example commands:

* Use `ls` to list nodes:
  ```
  [zk: localhost:2181(CONNECTED) 1] ls /
  [mesos, test2, zookeeper, marathon, test]
  ```

* Use `get` to see an individual node's contents:

  ```
  [zk: localhost:2181(CONNECTED) 15] get /test2
  hi
  cZxid = 0x2400000011
  ctime = Sat Apr 29 17:01:19 PDT 2017
  mZxid = 0x2400000011
  mtime = Sat Apr 29 17:01:19 PDT 2017
  pZxid = 0x2400000011
  cversion = 0
  dataVersion = 0
  aclVersion = 0
  ephemeralOwner = 0x0
  dataLength = 2
  numChildren = 0
  ```

You can also use `help` to see more commands. Note that you probably shouldn't
modify state in Zookeeper for Mesos or Marathon unless you know what you're
doing.
