[[!meta title="Slack"]]


We also offer IRC as a chat service. If that is what you were looking for head over
[[here|doc contact/irc]].

### Join the OCF Slack Workspace

Joining the OCF Slack requires an OCF account. If you don't have one already,
you can create one [here][join]. Head over to the [OCF Slack][slack] and create
an account with your <ocfusername>@ocf.berkeley.edu email address. This will
*only* work with an OCF email address. Note that your OCF email by default will
forward to your CalNet email address (e.g. oski@berkeley.edu). Using the
confirmation link in your email, you should now be able to set a display name
and password and join the OCF workspace. We recommend setting your display name
to your OCF username for consistency.

[join]: https://ocf.io/join
[slack]: https://fco.slack.com

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
