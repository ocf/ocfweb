[[!meta title="Request Tracker"]]

[**Request Tracker**](https://rt.ocf.berkeley.edu/) is the ticketing system
used by the OCF. It is the main way of keeping track of OCF-related activity.
Some tickets are automatically created when emails are received at the queue's
name (e.g. help@, devnull@, etc.). Staff can also create tickets by logging in
directly to the web UI.

## Queues
Tickets are assigned to queues, or organized boards. Manually-created
tickets are found under:
- *bod* for meeting topics
- *bureaucracy* for officer-related issues
- *operations* for Operations Strategist work (opstaff)
- *projects* for long-term activities
- *techtalks* for Tech Talk ideas and organization
- *todo* for shorter-term items

## Tickets
### Comment vs Reply
Much like the issues between Reply and Reply-All, the difference between Comment and Reply has led
to some mishaps. In the RT interface, *Reply* directly communicates with the poster, so look for the
last communication with the ticket opener. *Comment* doesn't directly communicate and is generally for
internal discussion. This can also be done through email, as RT defaults the reply-to field with the
queue mailing lists. Be careful here though: to comment through email, send the email to {queue}-comment
(i.e. help@ vs help-comment@). Also make sure that your reply does not include any of the comments, as in
make sure the trimmed comment is all the information you want released.

### Creation
They can be manually created through the *New Ticket in* button on the top right of the page. If doing
so to communicate to people outside of the OCF, add their email to the requestors field of the ticket and
leave the body blank. Afterwards, reply to the ticket to actually communicate with the person as the ticket
creation doesn't send emails to the requestor but does to staff.
Staff mailing lists are attached to the queue, so they usually don't have to be CC'd (i.e. *help* to help@).
You can set people to be owner, allowing people to keep track of assignments better.

### Modification
With any created ticket, it can be modified further. For queues like *bod*, some tickets should be discussed
more urgently than others. In the individual ticket page, one can change a ticket's priority value ([-10, 100]
recommended) by clicking on *The Basics*. Ownership is modified through *Reminders* and mailing list settings
can be modified through *People*.

Tickets may reference each other or there may be redundant tickets. If so, ticket relationships and merging
can be done under *Links* for the ticket you want to keep/set relations for.

#### Statuses
- *new*: New tickets without staff responses
- *open*: Responded tickets
- *stalled*: Held back due to other things. Turns to open on thread update.
- *resolved*: Manual resolution
- *rejected*: Rejection usually without comments
- *deleted*: Use sparingly, and generally used on obvious spam.

### Searching
By default, the queues only show *open* or *new* tickets. To see other tickets, either search the ticket number in the
top right or use *New Search* to do more advanced searching. If using the latter, don't forget to press either *Add these
terms and Search* or *Update formate and Search*. Search arguments can also be saved for later use, as seen with the
ocfstaff saved searches (bother a staff member to see these searches).
