[[!meta title="jessie migration"]]

This table lists all servers and whether they have been upgraded to jessie. In
general, we prefer to rebuild new servers using jessie, rather than upgrading
from wheezy. There are a few exceptions (marked as "upgrade" in the table).

We don't list the desktops (all are jessie already).

## Public facing servers:

Server         | Status | Comment
---------------|--------|---------------
pollution      | wheezy | rebuild - pykota not compatible with jessie on last attempt, not well puppeted

## Already upgraded:

Server         | Status | Comment
---------------|--------|---------------
jaws           | jessie | upgrade - kvm host
hal            | jessie | upgrade - kvm host
pandemic       | jessie | upgrade - kvm host
anthrax        | jessie | rebuild (no known issues)
blight         | jessie | rebuild
dementors      | jessie | rebuild - need to transfer some data (printer csv logs, munin data)
earthquake     | jessie | rebuild - need to update ocflib with new path to kadmin at same time
fallingrocks   | jessie | upgrade - mirrors
firestorm      | jessie | upgrade - ldap/kerberos, needs careful testing
lightning      | jessie | upgrade - puppet host
maelstrom      | jessie | upgrade - mysql host, needs testing first
pestilence     | jessie | rebuild - need to puppet first (want to move dns to git)
sandstorm      | jessie | upgrade - replacing with new mail service (rt#3068) which will be rebuilt
supernova      | jessie | upgrade - atool not well puppeted - still want to rebuild (rt#3676)
typhoon        | jessie | rebuild
zombies        | jessie | upgrade - some config not puppeted (csgo)
blackrain      | jessie | upgrade - hozer
blacksheep     | jessie | upgrade - hozer
despair        | jessie | upgrade - hozer
flood          | jessie | upgrade - hozer (irc)
gnats          | jessie | upgrade - hozer
kamikaze       | jessie | upgrade - hozer
limniceruption | jessie | upgrade - hozer
locusts        | jessie | upgrade - hozer
meltdown       | jessie | upgrade - hozer
meteorstorm    | jessie | upgrade - hozer
mudslide       | jessie | upgrade - hozer
quicksand      | jessie | upgrade - hozer
raptors        | jessie | upgrade - hozer
revolution     | jessie | upgrade - hozer
smallpox       | jessie | upgrade - hozer
death          | jessie | rebuild - complicated (rt#3524)
tsunami        | jessie | rebuild - same time as death (public)
