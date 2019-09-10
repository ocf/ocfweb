[[!meta title="Slack"]]


We also offer IRC as a chat service. If that is what you were looking for head over
[[here|doc contact/irc]].

### Join the OCF Slack Workspace

1. Create an OCF account [here][join].

2. Go to the OCF Slack workspace [here][slack] and click the "If you have an
   @ocf.berkeley.edu email address, you can create an account." button.

3. Enter your OCF username in the box, this should send an email to your Berkeley
   email. If you don't recieve an email, please contact a staff member for
   assistance.

4. Click the link in your Berkeley email and follow the instructions to complete
   setup. We *strongly* recommend setting your display name to your OCF username for
   consistency.

5. Join some channels!

[join]: https://ocf.io/join
[slack]: https://fco.slack.com

### List of Major OCF Channels

*#announcements*: Low volume announcements channel

*#administrivia*: Administrative discussion

*#henlo*: Social chat for current staff

*#ocf*: General alumni hangout channel and non-OCF tech discussion

*#rebuild*: Technical discussion

*#rebuild-spam*: Information on Github changes/PRs (spammy)

*#test*: Actual spam

### List of Minor OCF channels

*#cs162-fa19*, *cs170-fa19* and others: Per-class discussions

*#decal-general*: DeCal student chat

*#decalcomm*: DeCal administrative channel

*#stf*: OCF internal Student Tech Fund renewal discussion

*#xcf*: XCF discussion

### Optional: Using wee-slack

Note: This section is targeted at IRC users who would like to access Slack
using the `weechat` IRC client.

While our IRC network is bridged with Slack, some users prefer to use `weechat`
to connect directly to Slack. We already have `weechat` installed on `tsunami`,
so simply follow the instructions [provided by the wee-slack team][wee-slack].
Just make sure you are in a python virtual environment before running the
command:

```
python pip install websocket-client
```

We describe setting up a virtual environment [[here|doc
services/webapps/python]].  As a general recommendation, you'll probably want
to leave `wee-slack` running in a detached [tmux session][tmux].

[wee-slack]: https://github.com/wee-slack/wee-slack
[tmux]: https://linux.die.net/man/1/tmux
