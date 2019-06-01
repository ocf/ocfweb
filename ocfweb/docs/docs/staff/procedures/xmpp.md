[[!meta title="Manually creating XMPP accounts"]]

Currently, users must request XMPP accounts since registration is disabled. To
create an account for someone, you must have root privileges.

1. Ensure their email address matches the OCF username given
2. Generate a random password: `pwgen -s 16`
3. On `flood`, run the command
`sudo prosodyctl register username ocf.berkeley.edu password`
