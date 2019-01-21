[[!meta title="Installing updates with apt-dater"]]

Installing updates requires root (`ocfroot` group). Besides that, anybody
should feel free to install updates at any time. Generally it is quite safe,
though you might want to keep an eye on important things to ensure they start
again after being updated (MySQL, LDAP, and Kerberos are the common offenders).


## apt-dater

We install updates using [apt-dater](https://www.ibh.de/apt-dater/). We wrap it
in a script that builds a list of hosts from LDAP and sends a summary email to
root.

To install updates:

1. Make sure the desktops are not
   [suspended](https://github.com/ocf/puppet/blob/master/modules/ocf_desktop/files/suspend/ocf-suspend),
   and that you aren't trying to install updates near a 15-minute boundary when
   the desktops auto-suspend. See [[lab-wakeup|doc staff/howto/maintenance/lab-wakeup]] to
   wake up the desktops prior to updating.

2. From `supernova`, run:

       sudo apt-dater-ocf

   This will send an email to `root` with a list of packages to be updated.
   Glance over the list to make sure there are no obvious problems (for
   example, if it's trying to upgrade an entire system or install every
   available backport, which has actually happened before).

   Once apt-dater opens, proceed to the next step.

3. Select the "Updates pending" row at the top, and hit `u`. You'll be asked if
   you wish to upgrade the entire group. Press `y` to confirm.

4. All the hosts will now be in the "Sessions" category. Expand it (select then
   hit enter), then attach to each host one-by-one (hit `a` when you're over a
   host). You'll attach to a tmux session where the updates are being
   installed.

   In each session, wait for the updates to be installed, then press `C-b q`.
   If "errors" are found, you'll be asked to review them before proceeding.

   These are full tmux sessions, so you can, for example, use `Ctrl-B, D` to
   detach if your current session is taking a while.
