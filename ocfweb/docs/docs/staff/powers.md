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

In order to reset user passwords, staff must possess a `/root` principal. This
principal grants the staffer the ability to change users' passwords. This is
because chpass requires the Kerberos `change-password` privilege. The
permission to do this originates in the Kerberos administrative ACL
(`kerberos:/etc/heimdal-kdc/kadmind.acl`):

    username/root@OCF.BERKELEY.EDU change-password *@OCF.BERKELEY.EDU

This is usually given to staff after a semester of demonstrated interest.


## Technical managers

*group ocfroot*

The most technical and "on-call" staff members are given sudo access (root
privileges) on all servers and the ability to modify LDAP/Kerberos directly.

The Site Manager(s) and Deputy Site Manager(s) are always Technical Managers.
Other Deputy Managers and the General Manager(s) often happen to be Technical
Managers as well.

### `ocfroot` group

The ability to become root via sudo first requires the existence of a `/root`
principal (see above), with the exception of staff VMs where nobody needs a
`/root` (but it must either be *your VM* or you must be in group `ocfroot`).

Once that's satisfied, you must also be in the `ocfroot` LDAP group in order to
use `sudo` on most servers. (Exceptions: desktops and your staff VM don't
require you to be in ocfroot.)


### `/admin` principal

In order to modify LDAP or Kerberos, staff must possess a `/admin` principal
and it must be granted [Kerberos-editing rights in
Puppet](https://github.com/ocf/puppet/blob/master/modules/ocf_kerberos/files/kadmind.acl).
