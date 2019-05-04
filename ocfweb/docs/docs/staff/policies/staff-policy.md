[[!meta title="Staff policy"]]

Staff members shall be chosen by the OCF Decision Making Process. _[per OCF
Board decision on 4/13/89]_

_[The rest of this policy is per Site Manager decision on 8/30/17]_

## Background

The [[OCF Decision Making Process|doc
docs/operatingrules/constitution#ocf_decision_making_process]] spells out the
powers of BoD, the GMs, and the SMs; however, it doesn’t explain what powers
other staffers have.  The main purpose of this policy is to delineate what
things staff can do on their own, what things they must not do, and what things
they require special permission from the SM to do.

## Authorization

Staff are authorized to act independently of the SMs unless otherwise specified
here or elsewhere. This is so staff are not obstructed by having to ask the SMs
for approval for all decisions.

## Root privileges

The Site Managers have the sole power to add staff to the ocfroot group,
otherwise grant root privileges on a machine which runs a production service or
which mounts NFS, create and grant privileges to `/admin` principals, and grant
other powers which can be used to gain the aforementioned privileges or access
other OCF members’ data.

Staffers in the `ocfroot` group are known as Technical Managers.

To be eligible for Technical Manager status, you must fulfill the following
criteria:

* A Site Manager must be able to recognize you in person.
* You must have been a staffer for at least a semester already (although this
  requirement can be waived at the discretion of an SM).
* You must demonstrate a concrete, actual need for root privileges (e.g. a
  command you need to run which is blocking your OCF work).

The Site Managers can revoke Technical Manager status. This can happen, for
example, if root privileges aren’t actively being used.

If you are a Technical Manager, use your additional powers wisely. Remember
that you must respect the privacy of other members. In particular:

* Don’t read or modify a member’s files or directories unless one of the
  following is true:
   * The file or directory’s permissions ordinarily grant you access.
   * The member has requested it (explicitly or implicitly).
   * You have probable cause to suspect that the member may be involved in some
     policy violation (e.g. a security breach).
* The above restrictions also apply to surveilling members’ private activity
  on the OCF (e.g. by `strace`’ing their processes, recording network packet
  captures, etc.).
* If you do have to access a member’s files or other private data, limit your
  accesses to the minimum required to perform your duties.
* Let other members know when possible if modifying their files.

Here are some additional guidelines to follow:

* If you don’t have to use root for something, don’t use it.
* Avoid running an interactive shell as another user (or else you may cause
  undesirable side effects like polluting their `bash_history` or updating
  their last login time).
* Avoid using a root shell (i.e. `sudo -i`).

### Abuse of root privileges

The worst thing an OCF staffer could do is abuse root privileges. Abuse of root
privileges constitutes anything done using root privileges which is in
violation of OCF policies, University policies, or applicable laws. Examples of
this are violating members’ privacy (including reading or modifying their files
without reasonable cause), harassing members, maliciously logging people out,
deliberately compromising OCF security, etc. Abuse of root privileges may
result in consequences including, but not limited to, loss of root and/or staff
privileges, being banned from the OCF, and/or being referred to the Office of
Student Conduct.

## Amending of certain policies

There are some policies (e.g. this policy, the Unattended Processes Policy, …)
that the Site Managers have the power to amend. The SMs’ power to amend these
policies is not delegated to the Deputy Site Managers or any other staffer. In
other words, staffers cannot unilaterally make changes to these policies
without the SMs’ (or GMs’ or BoD’s) approval.

Site Managers should promptly inform staffers whenever they make amendments to
any such policies.
