[[!meta title="ShortURL guide"]]

We use `ocf.io` as a URL shortener.

One of its functions is to shorten member website URLs:
`https://ocf.io/username` is a shorturl for
`https://www.ocf.berkeley.edu/~username`.

We've additionally defined other shorturls. Here are some especially useful
ones for staff:

 * **ocf.io/gh/_<repo>_**, **ocf.io/github/_<repo>_**: The repository _<repo>_
   on the OCF GitHub page.\
   There are also abbreviations for the most commonly used repositories:
    * **ocf.io/gh/i**: ircbot
    * **ocf.io/gh/l**: ocflib
    * **ocf.io/gh/p**: puppet
    * **ocf.io/gh/u**: utils
    * **ocf.io/gh/w**: ocfweb
 * **ocf.io/rt**: RT
    * **ocf.io/rt/_<ticketnum>_**: The page for ticket _<ticketnum>_ in RT
 * **ocf.io/stats**: Lab stats
 * **ocf.io/guest**: If you bring a guest into the lab after hours, fill out
   this form
 * **ocf.io/servers**: The server chart
 * **ocf.io/bod**: BoD minutes

We also often give out these shorturls in RT tickets:

 * **ocf.io/join**: Signup page for an OCF account
 * **ocf.io/vhost**: Info about virtual hosting
 * **ocf.io/vhost-mail**: Info about mail virtual hosting
 * **ocf.io/apphost**: Info about apphosting

## More shorturls

You can find a full list of `ocf.io` shorturls in a table at
[ocf.io/shorturl](https://ocf.io/shorturl).
The shorturls are created in the Apache configuration via Puppet at
[ocf.io/shorturlpp](https://ocf.io/shorturlpp).

You can add additional shorturls to this list. When doing so, make sure that:

1. The shorturl isn't already someone's username, so you don't accidentally
   break the `ocf.io/username` functionality for them.
2. You add your shorturl to
   [the list of reserved usernames][reserved-usernames]. This way, no one will
   subsequently register an account with the same name as your shorturl and
   find that `ocf.io/username` doesn't work for them.

[reserved-usernames]: https://github.com/ocf/ocflib/blob/master/ocflib/account/validators.py
