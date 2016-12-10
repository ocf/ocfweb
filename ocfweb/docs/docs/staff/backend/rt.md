[[!meta title="Request Tracker"]]

[**Request Tracker**](https://rt.ocf.berkeley.edu/) is the ticketing system 
used by the OCF. It is the main way of keeping track of OCF-related activity. 
Tickets are currently made either by staff to propose things to talk about 
or by emails from the Hostmaster or Help mailing lists.

## Queues
Tickets are assigned to queues, or organized boards. Manually-created 
tickets are found under:
- *bod* for meeting topics
- *bureaucracy* for officer-related issues
- *operations* for Operations Strategist work (opstaff)
- *projects* for long-term activities
- *techtalks* for Tech Talk ideas and organization
- *todo* for shorter-term items

Other tickets are created automatically from emails:
- *devnull* for devnull@ emails
- *help* for questions from users (help@)
- *hostmaster* for requests for virtual hosting ([form](https://www.ocf.berkeley.edu/account/vhost/))
- *security* for vulnerability detections from ISP

All of these queues are also associated with a mailing alias.

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
 so to communicate to people outside of the OCF, add their email to the requestors field of the ticket. 
Staff mailing lists are attached to the queue, so they usually don't have to be CC'd (i.e. *help* to help@).
 You can set people to be owner, allowing people to keep track of assignments better.

### Modification
With any created ticket, it can be modified further. For queues like *bod*, some tickets should be discussed 
more urgently than others. In the individual ticket page, one can change a ticket's priority value ([-10, 100] 
recommended) by clicking on *The Basics*. Ownership is modified through *Reminders* and mailing list settings 
can be modified through *People*.

Tickets may reference each other or there may be redundant tickets. If so, ticket relationships and merging 
can be done under *Links* for the ticket you want to keep/set relations for.

Tickets are to be as *resolved* if done, *rejected* if not done for reasons, *new* on creation, and *open* otherwise.

### Searching
By default, the queues only show *open* or *new* tickets. To see other tickets, either search the ticket number in the 
top right or use *New Search* to do more advanced searching. If using the latter, don't forget to press either *Add these
 terms and Search* or *Update formate and Search*. Search arguments can also be saved for later use, as seen with the 
ocfstaff saved searches (bother a staff member to see these searches). 
