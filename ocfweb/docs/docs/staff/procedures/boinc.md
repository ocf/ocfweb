[[!meta title="Configuring BOINC"]]

In 2017, the OCF purchased a server intended for high-performance computing.
While the server is idle, we donate its capacity to SETI@home, hoping to find
the aliens before anyone else. SETI@home is a BOINC project, and BOINC will
happily use up 100% of CPU and GPU time, and this means the server can get
extremely loud (and hot).

## Accessing BOINC

The easiest way to control BOINC is to use the `boincmgr` GUI. Getting to the
GUI is, however, a multi-step process.

First, SSH and X-forward into the machine: at this time, our one HPC server is
named `corruption`.

    ssh -X corruption

Then, copy the output of `xauth list` into your clipboard/kill ring:

    $ xauth list
    corruption/unix:10  MIT-MAGIC-COOKIE-1  420053c541575e6b5e7f6119a2816016  # copy this

Then, open a root shell and paste the previously copied line after `xauth add`

    $ sudo -i
    abizer/root's password:
    root@corruption:~# xauth add corruption/unix:10  MIT-MAGIC-COOKIE-1  420053c541575e6b5e7f6119a2816016

Finally, type `boincmgr` to open the BOINC GUI manager on your desktop. From
the GUI one can then increase/decrease the amount of CPU time/resources BOINC
is using, to control the noise from corruption. One can also pause BOINC
entirely, add/remove projects, etc.
