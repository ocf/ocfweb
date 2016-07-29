[[!meta title="Internet Relay Chat (IRC)"]]


OCF staff often use IRC to communicate. If you have questions, feel free to
drop by &mdash; it's often faster than emailing us, especially for
discussion-type questions.

We normally chat in the `#rebuild` channel. For historical reasons, `#ocf` is
mostly for non-OCF-related discussion.

You have three simple options for chatting:

### Option 1: Use our web client

We have a web client set up at [irc.ocf.berkeley.edu][webirc] using the popular
open-source web client [The Lounge][thelounge]. It's already set up with our
IRC network settings, so all you need to do is enter a nickname that you want to
use and click the connect button at the bottom. You can enter your real name if
you want, but it's not required. Once connected, you can type messages in the
bottom bar and press enter and the OCF staff connected will respond to you as
soon as we see your messages.

### Option 2: Using your own client

You can connect using any IRC client. If you do not already have an IRC client,
we recommend using [Hexchat][hexchat] because it is free,
open source, and generally easy to use. Our server settings are listed below:

* **Server:** `irc.ocf.berkeley.edu`
* **Port:** `6697` (requires SSL/TLS)
* **Channels:** `#rebuild` (best to reach staff), `#ocf` (best for off-topic)

### Option 3: Over SSH

If you're logged in to the OCF login server via [[SSH|doc services/shell]], you
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
[NickServ module][nickserv] by running `/znc LoadMod nickserv` while connected
to your ZNC server. Then, in your ZNC web admin interface, log in and go to
`Your Settings` under either the global or user modules links. Under the
Networks section, click on the `Edit` link next to the OCF network and scroll
down to the Modules section. Enable the `nickserv` module and type the password
you used to register with NickServ into the arguments box. Then save your
changes using the button at the bottom of the page and ZNC should automatically
authenticate with NickServ if you get disconnected from ZNC.

[webirc]: https://irc.ocf.berkeley.edu
[thelounge]: https://thelounge.github.io
[hexchat]: https://hexchat.github.io
[nickserv]: http://wiki.znc.in/Nickserv
