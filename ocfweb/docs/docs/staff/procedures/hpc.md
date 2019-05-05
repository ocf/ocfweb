[[!meta title="Adding users to the HPC cluster"]]

Access to the OCF's HPC [[cluster | doc services/hpc]] is controlled by means
of an LDAP group named `ocfhpc`. If a user requests access to the cluster and
meets the basic access criteria, namely that they have specified what they
want to use the cluster for, simply run the following commands to add the user
to the LDAP group:

    abizer@supernova $ kinit abizer/admin ldapvi cn=ocfhpc
    ...
    memberUid: guser
    ...

Add another line to the list in the form of `memberUid: <username of requestor>`

Save and quit from your `$EDITOR`, and then reply to the request email with [this][hpc] template.

[hpc]: https://templates.ocf.berkeley.edu/#hpc-new-user
