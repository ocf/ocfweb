[[!meta title="Mesos"]]

At the OCF, we use [Mesos][mesos] and [Marathon][marathon] in order to deploy a
number of important services. This page will try to document how all of these
pieces fit together. The sub-pages are primarily troubleshooting steps and
instructions for working with each individual component.


## Mesos    {mesos}

**[Apache Mesos][mesos]** is software originally developed at Berkeley which
helps to schedule applications running on clusters of computers.

From reading the Mesos website, it's difficult to tell exactly what Mesos does
and does not do. The best way to think of Mesos is as a *scheduler*, which
determines how to run a set of applications across a cluster of computers.


### A Mesos cluster    {cluster}

A Mesos cluster consists of a small number of Mesos masters, and a large number
of Mesos agents (formerly called "slaves").

At the OCF, we have three Mesos masters:

* `mesos0` (`whirlwind`, running on `jaws`)
* `mesos1` (`pileup`, running on `pandemic`)
* `mesos2` (`monsoon`, running on `hal`)

At any given time, a Mesos cluster has only one *leader*, which is always one
of the Mesos masters. At any given time, only one of the masters is the leader,
and the other two masters are effectively doing no real work (but keeping track
of the work done by the leader, so that they can take over as leader if
necessary).

The cluster is considered healthy as long as a leader can be elected. A leader
can be elected as long as a majority of masters are online (quorum). At the
OCF, this means we must always have two masters online in order for Mesos to
function.

The reason a majority of masters must agree on a leader is to avoid the [split
brain problem][split-brain]. Imagine a network partition where `jaws`, `hal`,
and `pandemic` are all working, but `pandemic` becomes disconnected from the
network. Without the protection of requiring a majority of votes to elect a
leader, `jaws` and `hal` would hold one election, while `pandemic`, which is
isolated from the others, might elect itself leader. Now there are effectively
two separate clusters, with their own leaders, each trying to schedule tasks.
When the partition is corrected, how do we merge these two diverged clusters
back together? Requiring a majority election fixes this.

A Mesos cluster which becomes unhealthy will automatically recover as soon as
it can perform leader election. Because each Mesos master keeps a log of
actions of the current leader, any master can take over from the leader at any
time if necessary.

When a cluster is unhealthy, it will perform no work. It will not schedule new
tasks, provide offers to frameworks, etc.

The job of a Mesos master is *only to schedule tasks over the Mesos agents*.
Mesos masters never run any of the applications themselves, which is why our
Mesos masters are relatively low-powered machines.

A Mesos agent is a machine that offers resources to the current leading Mesos
master, and performs work that the leader tells it to do. Unlike masters, a
cluster can have hundreds of agents. We currently only have three:

* `jaws`
* `hal`
* `pandemic`

Internally, each Mesos agent provides *offers* to the Mesos master ("I have 10
CPUs, 200 GB of RAM, and 500 GB of disk space"). The master then decides what
to do with these offers.


### What Mesos actually does

As mentioned before, Mesos primarily concerns itself with scheduling, and not
the nitty-gritty details of running and supervising applications. Instead,
Mesos relies on *frameworks* (things like Marathon). When the Mesos master
receives an offer from a Mesos agent, it figures out how to fairly pass that
offer on to the various frameworks it runs.

At the OCF, we currently only run one framework (Marathon, discussed below).
Mesos will send the offer, along with additional metadata about the agent, to
the framework. It's up to the framework to decide whether to accept the offer,
and if it accepts, what to do with that offer.

Mesos agents can be tagged with metadata (such as `nfs:true`, to indicate the
agent has NFS available). This allows the framework to make intelligent
decisions about scheduling (such as knowing that certain applications can only
run on agents that have NFS).


## Marathon    {marathon}

**[Marathon][marathon]** is a framework running under Mesos. It's currently the
only one we use at the OCF.

Unlike Mesos, Marathon knows the intricate details about the services we run.
For example, the `ocfweb` service looks something like this:

```json
{
  "id": "/ocfweb/web",
  "cpus": 1,
  "mem": 1024,
  "instances": 3,
  "container": {
    "type": "DOCKER",
    "docker": {
      "image": "docker.ocf.berkeley.edu/ocfweb-web:2016-11-22-T16-33-01"
    }
  }
}
```

The application definition in reality is more complicated and contains
information about healthchecks, deployment constraints, etc.

Marathon's job is to figure out how to deploy all of our applications using the
offers given to it by the Mesos master.


### The Marathon masters    {masters}

Mesos frameworks like Marathon do not need to run on each Mesos agent. They
also do not need to run on each Mesos master. The only important thing is that
the framework runs *somewhere* and registers itself with the leading Mesos
master.

Some frameworks, like Marathon, provide a high-availability mode, which allows
the framework to run on several machines. At the OCF, we run Marathon on each
Mesos master (purely for convenience—there's no reason they couldn't be run on
any three random machines).

Like Mesos, only one Marathon master is leading at a given time, with the other
two basically doing no work. Unlike Mesos, Marathon uses Zookeeper (described
below) to perform both leader election and to store all configuration. *This
means that, unlike Mesos, it is not necessary to have a quorum of masters
running.* As long as the Zookeeper cluster is healthy, a single Marathon
instance is sufficient. Since all data is stored in Zookeeper, Marathon masters
themselves have no state.


## Zookeeper    {zookeeper}

**[Apache Zookeeper][zookeeper]** is effectively a highly robust distributed
key-value store. It is used as a primitive by many applications (including
Mesos and Marathon) to implement high-availability, though it can also be used
just as a regular key-value store.


### A Zookeeper cluster

A Zookeeper cluster consists of a number of masters, labeled by positive
integers `1` through `N`. Like Mesos, the cluster is only healthy when quorum
can be reached, meaning a majority of Zookeeper nodes are available. Here
again, there is only one leader, and the rest are followers.

Like with Marathon, there's no requirement that Zookeeper run on the Mesos
masters or agents. Again for convenience, we run three Zookeeper nodes, on the
three Mesos masters.

When addressing a Zookeeper cluster, the convention is to list all three nodes:

    zk://mesos0:2181,mesos1:2181,mesos2:2181/

Typically, a data path in the key-value store is specified after, such as
`/marathon` or `/mesos`. Tools that work with Zookeeper will use this path to
automatically figure out who the current leader is, even if some of the listed
nodes are down.


### How Mesos and Marathon use Zookeeper

Both Mesos and Marathon rely heavily on Zookeeper and cannot function without a
healthy Zookeeper cluster. Their usage of Zookeeper is slightly different, however.

Mesos does rely on Zookeeper for leader election, but not for storing its
state. Instead, it uses [Paxos][paxos] and a replicated log. This is why it is
necessary not just for the Zookeeper cluster to be healthy, but also to have a
quorum of Mesos masters, so that they can perform Paxos together.

By contrast, Marathon relies on Zookeeper for both election and state. This is
why Marathon can operate with only one master, as long as Zookeeper is healthy.

Zookeeper uses [Zab][zab], a similar protocol to Paxos, and has its own
replicated log. Fundamentally, Mesos could have been implemented the same way
Marathon is, relying on Zookeeper for leader election and storing state. For
whatever reason, it just isn't. In fact, they're planning to go the other
direction and [use their own Paxos implementation for leader
election][MESOS-3574], which would remove their requirement for Zookeeper at all.


[marathon]: https://mesosphere.github.io/marathon/
[mesos]: https://mesos.apache.org/
[split-brain]: https://en.wikipedia.org/wiki/Split-brain_(computing)
[zookeeper]: https://zookeeper.apache.org/
[paxos]: https://mesos.apache.org/documentation/latest/replicated-log-internals/
[zab]: https://cwiki.apache.org/confluence/display/ZOOKEEPER/Zab+vs.+Paxos
[MESOS-3574]: https://issues.apache.org/jira/browse/MESOS-3574
