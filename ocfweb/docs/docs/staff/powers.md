[[!meta title="Staff privileges"]]


OCF staff are members of the OCF who contribute their time as volunteers, and
are given responsibilities and privileges to maintain and improve the OCF's
infrastructure. There are many powers granted to staff, which for
simplification have been consolidated into a tiered structure.

Each tier includes the privileges of the preceding tiers.

Staff privileges are distinct from the Board of Directors, General Manager, and
Site Manager(s), which hold executive/legislative/judicial powers, although in
practice many staff members are Directors and vice versa.


## Staff

*group ocfstaff*

* receive `staff@ocf` mail (including staff discussions and announcements)
* can process group account requests
* can access and process [Request Tracker](https://rt.ocf.berkeley.edu/)
  tickets
* receive `wheel@ocf` mail (including  discussions with technical jargon)
* can change print quotas
* can login to all servers
* can edit shared staff files such as `User_Info` and `motd` (message of the
  day on public servers)
* can edit the [[wiki|doc staff/procedures/editing-docs]] and are expected to
  help maintain it
* must hold [[staff hours|staff-hours]], alongside other staffers
* must join a staffer family


### `/root` principal

In order to reset user passwords, staff must possess a `/root` principal.
Before student groups became able to reset their passwords online in 2015, this
principal was widely given out. However, since then, it has only been useful for
resetting passwords of group accounts with no associated signatories. It is now
given out as needed.


## Technical Managers

*group ocfroot*

The most technical and "on-call" staff members are given sudo access (root
privileges) on all servers and the ability to modify LDAP/Kerberos directly.

The Site Manager(s) and Deputy Site Manager(s) are always Technical Managers.
Other Deputy Managers and the General Manager(s) often happen to be Technical
Managers as well.

### `ocfroot` group
The ability to become root via sudo on machines other than your staff VM
requires the existence of a `/root` principal (see above).

You must also be in the `ocfroot` LDAP group in order to use `sudo` on most
servers. (Exceptions: desktops and your staff VM don't require you to be in
`ocfroot`.)

### `/admin` principal

In order to modify LDAP or Kerberos, staff must possess a `/admin` principal
and it must be granted [Kerberos-editing rights in
Puppet](https://github.com/ocf/puppet/blob/master/modules/ocf_kerberos/files/kadmind.acl).

### Other powers

Technical Managers also have the following powers:

 - Being in the Admin group in the OCF org on GitHub, which grants the ability
   to directly commit to any repository
 - Access to the RT admin interface
 - Admin privileges to the OCF status blog

Some Technical Managers, particularly the DSMs and SMs, may additionally have
the following:

 - Super admin status on Google Apps
 - Chanop status on IRC
 - Access to the firewall configuration interface
 - Being a Departmental Certificate Administrator for the InCommon certificate
   service
 - Knowledge of the root password
