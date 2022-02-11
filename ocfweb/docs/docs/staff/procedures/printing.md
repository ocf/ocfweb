[[!meta title="Printing maintenance"]]
## Removing printers from service

Ideally, printers shouldn't ever be turned off. Instead, they should be removed
from the CUPS classes:

1. Go to https://printhost.ocf.berkeley.edu/ (works only in lab)
2. Go to Classes > `double` > Modify Class
3. Remove the offending printer from the list of selected printers
4. GOTO 2, repeat for the `single` class

Alternatively, this can be done using the CUPS command `lpadmin` with proper authentication.

    lpadmin -p printername -r classname

The `printername` is the physical name of the printer (for example,
`logjam-double` or `logjam-single`) while the `classname` is the name
of the user-facing CUPS class (`double` or `single`).

(In theory pausing printers should have the same effect, but the current CUPS
version still queues jobs for them for some unknown reason, causing half of
user jobs to not print.)

## Restoring printer service

Perform the reverse of the above (add the printers back to the classes), then
double-check that the printers are not paused. This can also be done by
replacing the `-r` flag from the above command with `-c`.
Even if staff don't pause them,
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

## Recycling used toner

OCF goes through toners quite fast, due to the heavy volume of printing from our
users. In the past, we've let it accumulate inside the storage room which
resulted in accidental toner spillage. The following document contains how
to recycle the toners in hope of encouraging rapid removal of the toners from OCF space.

OCF staffers should keep an eye out for the accumulation of the toners, and proactively
recycle the used toners as soon as possible.

### Options to dispose the toners

* We can dispose the toners by returning them to
[Staples](https://www.staples.com/sbd/cre/marketing/sustainability-center/recycling-
services/) down at the Shattuck Ave. They give us $2 Staples rewards per toner, and
there is maximum limit of 10 toners per month. With the rewards, we can purchase
snacks and etc from Staples.
The rewards account information can be found in the passwd file.

* Copy Center at 3rd floor of Moffitt Library - to the right of FSM cafe when you enter the
building - would accept our toners that are individually sealed in a garbage bag.

* Xerox Recycles HP toners. One can [order](https://www.xerox.com/perl-bin/product.p
l?mode=recycling&XOGlang=en_US&referer=xrx) toner return box kit with a free return
label. Once the kit arrives, put the used toners in the box and schedule a UPS pick up.

## Performing maintenance on the printers

Our contract with PMP entitles us to free service for our printers, with a
short turn-around time. As a result, we should not longer attempt maintenance
ourselves, and should let the professionals take care of it. Should maintenance
be necessary, email `copycenter@library.berkeley.edu` (with `sm+printers@` cc'd)
to contact a PMP technician, inform them of the problem, and let them handle
everything else. Make sure to include the relevant printer IDs in the email. If
there are any questions about the terms of our service agreement, direct them to
the UC Berkeley PMP Coordinator.

The following is a list of our printers and their IDs, from left to right:

|  Printer name | ID # |
|---------------|------|
| papercut      | 1782 |
| logjam        | 1786 |
| pagefault     | 1781 |

## Stats

 * [Printer status Grafana dashboard (ocf.io/printers)][printer-dashboard]
 * Toner and Maintenance Kit [status][printer-summary]
 * [How many pages has each printer printed][pages-printed]? (expressed as total
   pages printed over time)


[toner]: https://www.staples.com/HP-64X-Black-Toner-Cartridge-CC364XD-High-Yield-Twin-Pack/product_821762
[pmp]: https://campuslifeservices.ucsf.edu/documentsmedia/services/print_management
[printer-dashboard]: https://ocf.io/printers
[printer-summary]: https://www.ocf.berkeley.edu/stats/
[pages-printed]: https://www.ocf.berkeley.edu/stats/printing/pages-printed
