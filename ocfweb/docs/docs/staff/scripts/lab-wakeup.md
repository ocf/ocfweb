[[!meta title="lab-wakeup: wake up suspended desktops"]]

## Introduction

##### Usage: `lab-wakeup $HOST`

Use `lab-wakeup $hostname` when you need to wake up a desktop that has
suspended. For example, if you try to SSH into `volcano.ocf.berkeley.edu`
 and get an error similar to

    ssh: connect to host $host port 22: No route to host

you can try `lab-wakeup volcano` on supernova or your staff VM to wake it,
after which you should be able to log in without issue. You may need to
install `wakeonlan` if it's not there already.

![](https://i.fluffy.cc/rLBlrNjrlnRN5tP9WjXjH8mkTss09fNH.png)

See also:
[ocf-suspend](https://github.com/ocf/puppet/blob/master/modules/ocf_desktop/file
s/suspend/ocf-suspend), which suspends the desktops on 15-minute intervals.
