[[!meta title="Staff mailing lists"]]

## Mailing lists

There are several mailing lists used internally by staff. Append
`@ocf.berkeley.edu` to the end of each mailing list.

All staffers are automatically added to the following two mailing lists:

 * `staff`: For staff announcements, such as meeting times and events.
 * `wheel`: For technical discussion among all staff

Staffers can also choose to be further added to the following mailing lists.
Technical Managers are required to join them:

 * `rt`: Emails sent to Request Tracker are copied to this mailing list. If
   you are on the `rt` mailing list, you can reply to RT tickets from your
   email. You are highly encouraged to join this mailing list even if you're
   not root staff.
 * `root`: Miscellaneous messages from system daemons are sent here:
    * Cron daemons send mail containing any stdout/stderr output from cronjobs
    * Munin sends mail whenever some munin measurement (e.g. disk usage, RAM
      usage, etc.) is outside the normal range
    * Jenkins sends emails whenever a Jenkins build fails
    * ocflib sends emails whenever an uncaught exception is thrown in ocfweb,
      create, enforcer, and several other background tasks
    * Miscellaneous other emails are sent here
   This mailing list gets a median of ~10 messages every day, although on some
   days it can get a lot more.
 * `puppet`: Error messages from puppet runs go here. This list tends to be
   very noisy.
 * `mon`: We've set up Rackspace Cloud Monitoring to email us alerts when our
   important services are inaccessible from outside the OCF network. Alerts
   from Rackspace get sent to this list.

On the administrative side, the `officers` mailing list receives emails related
to OCF administrivia. Cabinet members are expected to be on this mailing list,
and any other staffer can audit it as well.

Operations Staff are added to the `opstaff` mailing list.

<!-- TODO: uncomment when this list becomes official -->
<!-- Alumni are able to join the `alums` mailing list. Announcements -->
<!-- about alumni events and the like are sent here. -->

There are also some special purpose mailing lists:

 * `joinstaff`: we add emails from Calapalooza tabling to this mailing list, and
   send out announcements about our first staff meeting of the semester here.
   Announcements after the first staff meeting should be sent only to `staff`.

   This mailing list should be cleared every new semester.
