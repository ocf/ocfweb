[[!meta title="lab-wakeup: wake up suspended desktops"]]

## Introduction

##### Usage: `lab-wakeup $HOST`

Use `lab-wakeup $hostname` when you need to wake up a desktop that has suspended in order to SSH into it. For example, if you try to SSH into volcano.ocf.berkeley.edu and get an error similar to "ssh: connect to host $host port 22: No route to host" you can try `lab-wakeup volcano` on supernova or your staff VM to wake it, after which you should be able to log in without issue. If you're on your staff VM, you may need to install the wakeonlan package (`sudo apt-get install wakeonlan`) for the script to work.

![](https://i.fluffy.cc/rLBlrNjrlnRN5tP9WjXjH8mkTss09fNH.png)

See also: [ocf-suspend](https://github.com/ocf/puppet/blob/master/modules/ocf_desktop/files/suspend/ocf-suspend), which is the script that suspends the desktops on 15-minute intervals.
