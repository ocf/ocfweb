[[!meta title="Kerberos"]]

## Introduction

Kerberos is a network authentication system that is designed for client to
server communication over a (potentially) insecure network, where data can be
eavesdropped on, and addresses can be faked. It has several security and
usability advantages over using password-based authentication over the network.


### Security advantages

One major security advantage of using Kerberos is that if a ticket is stolen
from a host, it will expire, so damage is minimized compared to being able to
steal a password or long-lived ticket. Kerberos also assumes that the network
that is being used for communication could be compromised and has malicious
users who could be listening to network traffic and stealing any data sent from
machine to machine. To combat this, Kerberos does not send any data like
plaintext passwords or keys by themselves across the network that could be used
for attacks. Instead, it uses tickets, and encrypts data sent to clients and
servers with a key that only that machine can read.


### Usability advantages

Kerberos makes passwordless login easy, since after the first password is
input, a ticket can be used for future logins instead of having to type the
same password again and go through the whole authentication process a second
time. Keep in mind that all of the authentication will have to be done every 10
hours, as tickets do expire, but passwords have to be typed far less with
Kerberos in place. Tickets are invalidated on logout, so that makes sure that
someone can't steal a ticket and use it after you have left, as a little added
security.


## Versions

There are two major free versions of Kerberos: MIT and Heimdal Kerberos. At the
OCF, we use Heimdal Kerberos, so if you look up documentation, it might instead
be for the MIT version, so be careful to make sure the commands work. Kerberos
also has 2 main versions that are still used: version 4 and version 5. Version
5 fixes a lot of the security and design flaws of version 4, so we use version
5 of the protocol.


## Terminology

Unfortunately, Kerberos is a complicated protocol that involves a lot of
technical jargon. Here's a bunch of different terms that you might run into
when reading about or working on Kerberos and an attempt to explain what they
mean:

- **KDC** (**K**ey **D**istribution **C**enter): The central server that issues
  tickets for Kerberos communication and stores all user's keys. If the KDC is
  compromised, you are going to have a very bad time and [will not go to space
  today][xkcd-space]. Our current KDC is firestorm, but that could change in
  the future, as servers are moved around or rebuilt.

- **Realm**: A kerberos domain, usually identified with the domain name in all
  caps (e.g. `OCF.BERKELEY.EDU`). Two hosts are in the same realm if they share
  some kind of secret (password or key). The default realm is specified in
  `/etc/krb5.conf`, alongside the [location of the KDC and admin server]
  [kdc-location] (`kerberos.ocf.berkeley.edu` in our case). Cross-realm
  authentication is possible, but is thankfully not something we need to do, as
  it significantly complicates things.

- **Principal**: A Kerberos principal is essentially a name used to refer to an
  entry in the Kerberos database. Each principal is associated with a user,
  host, or service of a realm. All principals shown below are followed by
  `@OCF.BERKELEY.EDU` since it is the realm the OCF uses.

  - **User**: `[user]` or `[user]/[instance]` e.g. `jvperrin` or
    `mattmcal/root`. Used for user logins or for user privileges such as
    editing LDAP or running commands with `sudo`.

  - **Host**: `host/[hostname]` e.g. `host/supernova.ocf.berkeley.edu`. Used by
    Kerberos to allow clients to verify they are communicating with the correct
    host. For instance, when using SSH to connect to a host, that hosts's
    principal is looked up to make sure that you are connecting to the right
    host and that the host is not actually some other malicious host.

  - **Service**: `[service]/[hostname]` e.g. `ldap/firestorm.ocf.berkeley.edu`.
    Used to enable Kerberos authentication with a service running on a
    particular host, such as `http`, which (for instance) enables logins to RT,
    or `smtp`, which allows email authentication.

- **Ticket**: Tickets are issued by the TGS (see below) to clients. Tickets
  have an expiration time, which is set to the default of 10 hours after being
  issued.

- **Keytab**: A keytab is essentially the equivalent of a password, but one
  that can be used easily by a script. If someone has read access to a keytab,
  they can retrieve all the keys in it, so be very careful what permissions are
  set on keytabs.

- **TGT** (**T**icket **G**ranting **T**icket): A special ticket that is used
  for communication between the client machine and the KDC.

- **TGS** (**T**icket **G**ranting **S**ervice): Usually the same as the KDC,
  the job of the TGS is to grant tickets (see above) for different network
  services.

- **GSS-API**: The API used by different applications to be able to
  authenticate with Kerberos.

- **SASL**: An authentication layer that many different applications can use.

[xkcd-space]: https://xkcd.com/1133/
[kdc-location]: https://github.com/ocf/puppet/blob/master/modules/ocf/files/auth/krb5.conf#L27


## Commands

All conveniently prefixed with the letter `k`.

- `kinit`: Used to get a ticket, for instance to be able to edit LDAP, or run
  commands that need `sudo` (using the `[user]/root` principal). For instance,
  to edit your own LDAP entry, run `kinit [user]/admin ldapvi uid=[user]` to
  authenticate using your `admin` Kerberos principal and then run `ldapvi`. The
  default principal requested is your base user principal (`[user]@[realm]`).
  Any commands put after `kinit` will be ran as usual with the requested
  credentials.

- `klist`: Shows all current tickets held with issued and expiration datetimes
  and the principal that each ticket corresponds to.

- `kadmin`: Administration utility for Kerberos to make changes to the Kerberos
  database, either locally (with `-l`), or remotely by connecting to the KDC.
  Can retrieve information about principals, modify principal attributes,
  change principal passwords, show privileges allowed, etc.

- `kdestroy`: Remove a principal or ticket file. This is essentially the
  opposite of `kinit`, so it invalidates tickets you have, logging you out from
  Kerberos. This is automatically run on logout to invalidate any lingering
  tickets.

- `ktutil`: Very useful command that has a variety of subcommands for managing
  keytabs. Can be used to list credentials available in a keytab, add keys to a
  keytab, remove keys, etc.

- `kpasswd`: Used to change Kerberos passwords.

- `kimpersonate`: Used for impersonating another user using their keytab.

There are more commands, but they aren't used so often, and can be searched if
needed.


## Adding privileges for users

To add privileges for users, first create a new principal for them to use. As
part of this process, the user will have to give each principal a password. The
password can be the same or different from their main user principal, but they
will have to enter it every time they want to edit LDAP or run commands with
`sudo`. To create a new principal, run `kadmin add [user]/[instance]`, where
`[instance]` is either `root` or `admin`. The `[user]/root` principal is used
when running `sudo` commands and for changing user passwords, whereas the
`[user]/admin` principal is used mainly for modifying LDAP.

Next, to give the principal actual privileges, add the principals and
privileges assigned to the [kadmind.acl file][2] used by Puppet. Notice that
the `all` privilege does not actually give *all* privileges, since the
`get-keys` privilege is separate.  The `get-keys` privilege is used to fetch
principals' keys, which is equivalent to knowing the password hash in other
authentication systems, so it is not a privilege to be handed out lightly.

[2]: https://github.com/ocf/puppet/blob/master/modules/ocf_kerberos/files/kadmind.acl


## How does it actually work?

Kerberos is pretty complicated, so explaining exactly how it works gets messy
very quickly, but here are the main steps that are taken by Kerberos when a
user logs in to their machine. A great guide on these steps is [Lynn Root's
_Explain it like I'm 5: Kerberos_][eli5], and explains it better and in more
depth than the rather cursory overview found here:

1. The user enters their username. Their login is sent to the KDC to receieve a
   ticket.

2. The KDC checks in its database for a principal that matches the one sent by
   the client. If one is found, it returns a TGT, which is encrypted with the
   user's key (originally generated from the user's password and stored on the
   KDC).

3. The client gets the encrypted TGT and decrypts it with the user's entered
   password. Note the user's password was never directly sent across the
   network at any stage in the process. Then the TGT is stored in the cache on
   the client machine until it expires, when it is requested again if needed.

4. The user can then use this TGT to make requests for service tickets from the
   KDC.

Kerberos makes sure that nobody can request a TGT for a user except the user
themselves by using preauthentication, which essentially means that the KDC
requests additional authentication than just a principal to give a TGT, since
otherwise the key in the TGT could just be cracked offline by an attacker using
a dictionary attack. This preauthentication typically takes the form of
something like the current time encrypted with the user's key. If an attacker
intercepts this communication, they do not have the exact timestamp or the
user's key to attempt to decrypt it. We require pre-authentication at the OCF
by specifying `require-preauth = true` in [/var/lib/heimdal-kdc/kdc.conf][kdc].

Then, if the user wants to communicate with other services or hosts, like SSH
or a HTTP Kerberos login, then they make more requests to the KDC:

1. The client will request a service or host principal from the TGS (Ticket
   Granting Service) using the TGT received before. The TGS in our case is the
   same as the KDC, but for some systems they could be different hosts. The TGS
   sends in response a service ticket, which the client then stores for use in
   contacting a service and authenticating until the service ticket expires.

2. The client can then use this service ticket to send with requests to
   Kerberos-enabled services, like SSH, as user authentication. The service
   will verify the ticket with the KDC when used, to make sure it is valid for
   the user issuing the request.

[eli5]: http://www.roguelynn.com/words/explain-like-im-5-kerberos/
[kdc]: https://github.com/ocf/puppet/blob/master/modules/ocf_kerberos/files/kdc.conf#L13
