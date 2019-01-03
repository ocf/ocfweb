[[!meta title="Restarting services"]]

## Taking production services offline

_As established by the SMs on August 30, 2017._

Staffers who wish to take any production service offline for longer than the
length of a reboot, or who wish to reboot a hypervisor hosting production
services must gain permission from the Site Managers or Deputy Site Managers
whenever possible.

Whenever a staffer restarts a production service, whether permission is
required or not, or restarts a machine that other users have running processes
on, they must give notice to other staffers of their actions as soon as
possible and ideally receive acknowledgement. The staffer should preferably do
this on IRC/Slack.

Staffers scheduling downtime for public-facing services should make a blog post
at [status.ocf.berkeley.edu][status] to give users sufficient advance notice.
Planned restarts of hypervisors should also be announced on this blog, since
restarting hypervisors can often take several minutes or more.

_End of policy_

## Rebooting hypervisors

Rebooting hypervisors is a slightly risky business. Hypervisors aren't
guaranteed to always reboot without problems. Therefore, you shouldn't reboot
them unless you can physically access the lab in case problems arise.
Additionally, this risk is the reason (D)SM permission is normally required to
reboot hypervisors.

So you've gotten the necessary permission and made a post on the
[status blog][status]/updated the MOTD (if it's a scheduled restart). What now?

If you are planning to shut down login servers (i.e. tsunami, werewolves and
corruption), run the `shutdown` command on these machines as soon as possible in
order to schedule the shutdown and warn users in advance. You can do this with
a command like

    sudo shutdown -h 22:00 "Rebooting for kernel upgrades"

for a shutdown scheduled for 10:00pm.

For other VMs, you can shut them each down via `sudo virsh shutdown`.

Be careful to **always shut down firestorm last**. This is because once
firestorm is shut down, LDAP/Kerberos logins go offline, and the hypervisors can
thereafter only be logged into via the root account. Since you'll not be able to
run new commands using sudo, you should always `sudo -i` before shutting down
firestorm.

Once all of the VMs have been shut down, you can then power off the hypervisors
via `shutdown -h now`.


[status]: https://status.ocf.berkeley.edu
