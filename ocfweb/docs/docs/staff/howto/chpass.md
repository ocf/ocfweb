[[!meta title="chpass: reset a user's password"]]

The preferred way of changing passwords is to [[do it online|change_password]].
This does not require a staffer to be present to change the user's password.
Only use the command line chpass if this is not suitable. An example is, for
group accounts or users that send notarized letters to the OCF.

## Technical Description

Python script that changes a user's kerberos principal password using a specified
staff/root principal.

## Usage

    ~$ chpass andromeda

Changes user andromeda's password

## Sample Use Case

You can run chpass on any server.

    raphtown@pileup:~$ chpass andromeda
    OCF Change Password Program

    WARNING: If you are resetting/changing a password for an OCF staff member,
    you acknowledge that you may potentially modify some of the privileges that the staff
    member may have.

    Changing password for: andromeda:*:1615:20:Andromeda Centauri,The OCF,,:/home/a/an/andromeda:/opt/share/utils/bin/sorried

Let the user type in his new password (and verify it). Requirements are for
passwords to be at least 8 characters long. It is helpful to indicate that
nothing will show up when the user starts typing.

    Enter New Password:
    Verify password:
    Connecting to kerberos.ocf.berkeley.edu...

Now type in your kerberos root principal password. If you don't have one you
can't change passwords!

    Please enter the password for principal raphtown/root:
    andromeda@OCF.BERKELEY.EDU's Password:
    Verifying - andromeda@OCF.BERKELEY.EDU's Password:
    raphtown/root@OCF.BERKELEY.EDU's Password:
    Successfully changed heimdal kerberos principal
