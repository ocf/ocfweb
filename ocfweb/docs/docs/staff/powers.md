[[!meta title="Staff privileges"]]

# Staff privileges

OCF staff are members of the OCF who contribute their time as volunteers, and are given responsibilities and privileges to maintain and improve the OCF's infrastructure. There are many powers granted to staff, which for simplification have been consolidated into a tiered structure.

Each tier includes the privileges of the preceding tiers.

Staff privileges are distinct from the Board of Directors, General Manager, and Site Manager(s), which hold executive/legislative/judicial powers, although in practice most staff members are Directors and vice versa.

[[!toc startlevel=2]]

## Staff
*group approve*

Newly-interested staff members are given basic training on [[OCF scripts|scripts]] and added to group `approve`.

* receive `staff@ocf` mail (including staff discussions and announcements)
* can process group account requests
* can access and process [Request Tracker](https://rt.ocf.berkeley.edu/) tickets
* can login to the print server
* can post staff hours alongside a more privileged staff member (shadowing)

## Privileged staff
*group ocfstaff*

Staff members who demonstrate long-term commitment and proficiency are given additional training, elevated privileges, and responsibilities. Most staff members are expected to graduate into this category.

* receive `wheel@ocf` mail (including cron spam and discussions that include mundane technical jargon)
* can change print quotas
* can login to all servers
* have sudo access (root privileges) on the print server
* can edit shared staff files such as `User_Info` and `motd` (message of the day)
* can edit the [[wiki|ikiwiki/editing-the-wiki]] and are expected to help maintain it
* must hold staff hours
* can reset account passwords (see below)

### `/root` principal

In order to reset user passwords, staff must also possess a `/root` principal. This principal grants the staffer the user the ability to change passwords. This is because chpass requires the Kerberos `change-password` privilege. The permission to do this originates in the Kerberos administrative ACL (`kerberos:/etc/heimdal-kdc/kadmind.acl`):

    username/root@OCF.BERKELEY.EDU change-password *@OCF.BERKELEY.EDU

## Technical managers
*group ocfroot*

The most technical and "on-call" staff members are given sudo access (root privileges) on all servers and the ability to modify LDAP/Kerberos directly.

This usually corresponds to Deputy Manager(s) and Site Manager(s). Sometimes the General Manager may also act as a Deputy Manager.

### `ocfroot` group

The ability to become root via sudo first requires the existence of a `/root` principal (see above).

This originates from PAM configuration at `/etc/pam.d/sudo` and `/etc/sudoers`.

`/etc/pam.d/sudo`:

    auth required pam_krb5.so minimum_uid=1000 alt_auth_map=%s/root only_alt_auth

`/etc/sudoers`:

    %ocfroot ALL=(ALL) ALL

### `/admin` principal

This principal can be used to modify LDAP and Kerberos.

#### ldapmodify

The ability to write to LDAP originates in OpenLDAP configuration (`ldap:/etc/ldap/slapd.conf`):

    # Allow read over SSL or Kerberos, and write by only admins
    access to * by sasl_ssf=56 dn.regex="^uid=[^,/]+/admin,cn=GSSAPI,cn=auth$$" write

#### kadmin

The ability to write to Kerberos originates in the Kerberos administrative ACL (`kerberos:/etc/heimdal-kdc/kadmimd.acl`):

    username/admin@OCF.BERKELEY.EDU all
