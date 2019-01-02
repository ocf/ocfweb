[[!meta title="Printing maintenance"]]
## Removing printers from service

Ideally, printers shouldn't ever be turned off. Instead, they should be removed
from the CUPS classes:

1. Go to https://printhost.ocf.berkeley.edu/ (works only in lab)
2. Go to Classes > `double` > Modify Class
3. Remove the offending printer from the list of selected printers
4. GOTO 2, repeat for the `single` class

(In theory pausing printers should have the same effect, but the current CUPS
version still queues jobs for them for some unknown reason, causing half of
user jobs to not print.)

## Restoring printer service

Perform the reverse of the above (add the printers back to the classes), then
double-check that the printers are not paused. Even if staff don't pause them,
CUPS will pause them automatically if they fail.

## Replacing toner

Toner replacement takes only a few seconds. Don't bother recording toner
replacement, there is no point.

Old toner cartridges should be saved in the server room (find a box that has a
bunch of old toner in it). We return these to Staples for $2/cartridge in
rewards.

Our printers use [CC364X toner cartridges][toner]. As part of our service
agreement with the [UCSF Print Management Program][pmp], we buy toner in bulk
from them and in exchange receive complimentary service for our printers. In
order to replenish stocks of toner, first get in touch with the UC Berkeley
PMP Coordinator (as of 2018, this is Pam Krol) to get a quote for a bulk toner
order, and then notify our LEAD Center advisor to get the pass-through account
chartstring in order to let PMP debit our account directly through the ASUC.
Once a contract is signed, PMP will ship the toner to the lab and withdraw
funds from our account automatically. It is necessary to inform our advisors
of this in advance so they can properly authorize and document the fund transfer
between the ASUC and the University. The LEAD center has requested we keep our
use of the passthrough account to a miminum, so we've agreed to buy toner in
annual intervals.

## Performing maintenance on the printers

Our contract with PMP entitles us to free service for our printers, with a
short turn-around time. As a result, we should not longer attempt maintenance
ourselves, and should let the professionals take care of it. Should maintenance
be necessary, follow the instructions on the stickers attached to the front of
the printers to contact a PMP technician, inform them of the problem, and let
them handle everything else. If there are any questions about the terms of our
service agreement, direct them to the UC Berkeley PMP Coordinator.


## Stats

 * [Printer status Grafana dashboard (ocf.io/printers)][printer-dashboard]
 * Toner and Maintenance Kit [status][printer-summary]
 * [How many pages has each printer printed][pages-printed]? (expressed as total
   pages printed over time)


[toner]: http://www.staples.com/HP-64X-Black-Toner-Cartridge-CC364XD-High-Yield-Twin-Pack/product_821762
[pmp]: http://campuslifeservices.ucsf.edu/documentsmedia/services/print_management
[printer-dashboard]: https://ocf.io/printers
[printer-summary]: https://www.ocf.berkeley.edu/stats/
[pages-printed]: https://www.ocf.berkeley.edu/stats/printing/pages-printed
