[[!meta title="Internet Relay Chat (IRC)"]]


OCF staff often use IRC to communicate. If you have questions, feel free to
drop by -- it's often faster than emailing us, especially for discussion-type
questions.

We normally chat in the `#rebuild` channel. For historical reasons, `#ocf` is
mostly for non-OCF-related discussion.

You have two simple options for chatting:

### Option 1: Using your own client

You can connect using any IRC client:

* **Server:** `irc.ocf.berkeley.edu`
* **Port:** `6667` (non-SSL), `6697` (SSL)
* **Channels:** `#rebuild` (best to reach staff), `#ocf` (best for off-topic)

### Option 2: Over SSH

If you're logged in to the OCF login server via SSH, you can use the pyrc
script to easily connect to IRC. It will automatically launch a tmux session to
contain your IRC session, so that you aren't disconnected when you close the
terminal.

To do so, just type `pyrc` and hit enter. irssi will launch; press alt +
left/right to switch which channel you're viewing.
