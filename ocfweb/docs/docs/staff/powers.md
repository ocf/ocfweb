[[!meta title="Staff privileges"]]


OCF staff are members of the OCF who contribute their time as volunteers, and
are given responsibilities and privileges to maintain and improve the OCF's
infrastructure. There are many powers granted to staff, which for
simplification have been consolidated into a tiered structure.

Each tier includes the privileges of the preceding tiers.

Staff privileges are distinct from the Board of Directors and Officers, which
hold legislative and executive powers respectively, although in practice
virtually all Directors are staffers.


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
* can directly edit the OCF website and commit to some other repositories,
  such as slackbridge, templates, and utils, and are expected to maintain them
* must hold [[staff hours|staff-hours]], alongside other staffers
* must join a staffer family


### `/root` principal

In order to reset user passwords, staff must possess a `/root` principal.
Before RSOs became able to reset their passwords online in 2015, this principal
was widely given out. Since then, it has become much less necessary to have for
staff hours. It is now given out as needed.


## Technical Managers

*group ocfroot*

The most technical and "on-call" staff members are given sudo access (root
privileges) on all servers and the ability to modify LDAP/Kerberos directly.

The Site Manager(s) and Deputy Site Manager(s) are always Technical Managers.
Other Deputy Managers and the General Manager(s) often happen to be Technical
Managers as well.

### `ocfroot` group

You must be in the `ocfroot` LDAP group in order to use `sudo` on most
servers, other than desktops and your own staff VM.

The ability to become root via sudo on machines other than your staff VM
requires the existence of a `/root` principal (see above).

### `/admin` principal

In order to modify LDAP or Kerberos, staff must possess a `/admin` principal
and it must be granted [Kerberos-editing rights in
Puppet](https://github.com/ocf/puppet/blob/master/modules/ocf_kerberos/files/kadmind.acl).

### Other privileges

Technical Managers also have the following privileges:

* Being in the Admin group in the OCF org on GitHub, which grants the ability
  to directly commit to any repository
* Access to the RT admin interface
* Admin privileges to the OCF status blog

Some Technical Managers, particularly the DSMs and SMs, may additionally have
the following:

* Being an Owner of the GitHub OCF org
* Super admin status on Google Apps
* Chanop status on IRC
* Services Root Adminship for Anope
* Access to the firewall configuration interface
* Being a Departmental Certificate Administrator for the [InCommon certificate
  service](https://cert-manager.com/customer/incommon)
* Knowledge of the root password
* Access to [NetReg](https://netreg.berkeley.edu/)
* Access to view Google Analytics data for ocfweb
