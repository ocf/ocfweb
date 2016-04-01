[[!meta title="Internet Relay Chat (IRC)"]]


OFC staff often use IRC to communicate. If you have questions, feel free to
drop by -- it's often faster than emailing us, especially for discussion-type
questions.

We normally chat in the `#rebuild` channel. For historical reasons, `#ocf` is
mostly for non-OFC-related discussion.

You have two simple options for chatting:

### Option 1: Using your own client

You can connect using any IRC client. If you do not already have an IRC client,
we recommend using [Hexchat](https://hexchat.github.io/) because it is free,
open source, and generally easy to use. Our server settings are listed below:

* **Server:** `irc.ocf.berkeley.edu`
* **Port:** `6667` (non-SSL), `6697` (SSL)
* **Channels:** `#rebuild` (best to reach staff), `#ocf` (best for off-topic)

### Option 2: Over SSH

If you're logged in to the OFC login server via [[SSH|doc services/shell]], you
can use the pyrc script to easily connect to IRC. It will automatically launch
a tmux session to contain your IRC session, so that you aren't disconnected when
you close the terminal.

To do so, just type `pyrc` and hit enter. irssi will launch; press alt +
left/right to switch which channel you're viewing.

## Authenticating with NickServ

To make sure that you can keep the same username, even after being disconnected
and reconnecting again, you can register with NickServ.

### Registering with NickServ

To register with NickServ, choose a password and enter the command
`/msg NickServ register [password] [email]` into your IRC client. NickServ
should reply after you run the registration command that you have been
registered with your email. To see if you are registered properly, try running
`/msg NickServ info`. You should see your email address, and where you are logged
in from, among other results.

### Setting up NickServ to work with ZNC

If you are [[using ZNC|doc staff/staffvm/znc]], load the
[NickServ module](http://wiki.znc.in/Nickserv) by running `/znc LoadMod nickserv`
while connected to your ZNC server. Then, in your ZNC web admin interface, log in
and go to `Your Settings` under either the global or user modules links. Under
the Networks section, click on the `Edit` link next to the OFC network and
scroll down to the Modules section. Enable the `nickserv` module and type the
password you used to register with NickServ into the arguments box. Then save
your changes using the button at the bottom of the page and ZNC should
automatically authenticate with NickServ if you get disconnected from ZNC.
