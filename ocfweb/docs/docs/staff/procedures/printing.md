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

Our printers use [CC364X toner cartridges][toner]. We usually purchase the
CC364XD item (same thing, but a dual pack) since it's usually cheaper. Other
sellers (e.g. Amazon) are often significantly cheaper than Staples, but it
varies a lot. We try to purchase in bulk when we find them at low cost.

## Replacing maintenance kits

We normally replace maintenance kits on schedule, although they can print past
the official limit. (Print quality might start to suffer, and it might not be
great for the printers, though.)

Replacing maintenance kits is best done after lab hours, since it requires
access to the back of the printer (and can be disruptive).

The instructions provided with the maintenance kits are quite nice and have
diagrams to follow showing where to replace the different parts in the printer.
Gloves are provided with the kit, but using them is not necessary. However,
they are good to use when replacing parts that have ink on them though to
protect your hands and the part being replaced. The maintenance kits have more
rollers provided than the printers use, so don't worry if you have a lot of
them left over after replacing the kit.

The most complicated part of the kit replacement is actually resetting the
maintenance kit warning on the printer after it is all installed. To reset the
warning, turn off the printer using the power switch on the lower right. Then,
turn on the printer and hold down the `OK` button while the printer is starting.
Once the printer stops loading any further, release the `OK` button and a
startup menu should appear. In this menu, select `NEW MAINTENANCE KIT` and press
the `OK` button and the printer should proceed to start normally with the
warning reset.

Our printers use [CB388A maintenance kits][maintkit].

## Stats

 * [How much toner is left in each printer][oracle]? (expressed as approximate
   pages remaining over time)
 * [How many pages has each printer printed][historacle]? (expressed as total
   pages printed over time)


[toner]: http://www.staples.com/HP-64X-Black-Toner-Cartridge-CC364XD-High-Yield-Twin-Pack/product_821762
[maintkit]: http://www.staples.com/office/supplies/StaplesProductDisplay?storeId=10001&partNumber=854426
[oracle]: http://stats.ocf.berkeley.edu/printing/oracle/
[historacle]: http://stats.ocf.berkeley.edu/printing/historacle/
