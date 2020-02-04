[[!meta title="Slack"]]


We also offer IRC as a chat service. If that is what you were looking for, head
over to [[our page on IRC|doc contact/irc]].

### Join the OCF Slack Workspace

1. [Create an OCF account][join] if you don't yet have one.

2. Go to the [OCF Slack workspace][slack] and click the "If you have an
   [[@ocf.berkeley.edu email address|doc services/mail]], you can create an
   account." button.

3. Enter your OCF username in the box, this should send an email to your Berkeley
   email. If you don't recieve an email, please contact a staff member for
   assistance.

4. Click the link in your Berkeley email and follow the instructions to complete
   setup. We *strongly* recommend setting your display name to your OCF username for
   consistency.

5. Join some channels!

[join]: https://ocf.io/join
[slack]: https://fco.slack.com

### Other important info

#### Everything is public

When using Slack, please keep in mind that the channels are connected to our
[[IRC server|doc contact/irc]], which is open to the whole world. Anyone could
be keeping a log of what is said, so please don't say anything that you wouldn't
want to be public!

#### I can't log in!

When logging in, don't use your `@berkeley.edu` email. Instead, use [[your OCF
email address|doc services/mail]], which is `<OCF username>@ocf.berkeley.edu`.
If you're still having trouble, you can always reset your password.

### List of Major OCF Channels

*#announcements*: Low volume announcements channel. Turn on notifications for
messages in this channel (instructions for [desktop][desktop-notifications] and
[mobile][mobile-notifications])!

[desktop-notifications]: https://slack.com/help/articles/201355156-Guide-to-desktop-notifications#channel-specific-group-dm-notifications
[mobile-notifications]: https://slack.com/help/articles/360025446073-Guide-to-mobile-notifications#channel-specific-group-dm-notifications

*#rebuild*: Technical discussion

*#administrivia*: Administrative discussion

*#henlo*: Memes and off-topic social chat with current staff

*#ocf*: General alumni/staff off-topic hangout channel and non-OCF tech
discussion

*#rebuild-spam*: Information on Github changes/PRs (spammy)

*#test*: Actual spam

### List of Minor OCF channels

*#decal-general*: DeCal student chat

_#\*-comm_: Channels for committee discussion

*#cs162-fa19*, *cs170-fa19*, and others: Per-class discussions

*#xcf*: XCF discussion

### Optional: Using wee-slack

Note: This section is targeted at IRC users who would like to access Slack
using the `weechat` IRC client.

While our IRC network is bridged with Slack, some users prefer to use `weechat`
to connect directly to Slack. We already have `weechat` installed on `tsunami`,
so simply follow the instructions [provided by the wee-slack team][wee-slack].
Just make sure you are in a python virtual environment before running the
command:

```bash
python pip install websocket-client
```

We describe setting up a virtual environment [[here|doc
services/webapps/python]].  As a general recommendation, you'll probably want
to leave `wee-slack` running in a detached [tmux session][tmux].

[wee-slack]: https://github.com/wee-slack/wee-slack
[tmux]: https://linux.die.net/man/1/tmux
