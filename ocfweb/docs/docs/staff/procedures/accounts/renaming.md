[[!meta title="Rename an account"]]

We should sparingly rename a user account, and only do so when it is
necessary (e.g. typo in the username or update of their lived name).

To rename an individual account, `sorry` the account with the old name and
make a `note` of why you are changing the username. To run `sorry` you need
to be a root user. Follow the prompts of the script.

```bash
sudo sorry username_to_rename

note -u username_to_rename
```

Then manually create an
account using `approve`. [[Associate|doc staff/procedures/accounts/association]]
the user's `calnetUID` manually, and delete `callinkOID` attribute. You will need
to be a root user to do this. Be sure to `note` the reason and previous username
in the new account note file.

```bash
approve

note -u new_username
```

#### Note
When the user uses certain OCF webpage (e.g. password reset) that uses `calnetUid`
to find associated OCF accounts, the user will see their old account in the
list of accounts drop-down menu. However, as the old account has been sorried,
the user cannot use the old account in any ways.
