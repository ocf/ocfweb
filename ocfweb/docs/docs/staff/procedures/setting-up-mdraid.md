[[!meta title="Setting up mdraid on servers"]]

Setting up a new server involves putting in all its new drives, turning off
MegaRAID, setting up mdraid (Linux software RAID) on them, and then installing
the operating system.  It requires quite a few tricky steps.

The below steps were written for jaws/pandemic/hal which have LSI RAID cards
that need to be put into JBOD mode. The intructions will vary without LSI
hardware RAID (which we don't use).

Also, MegaCLI isn't very consistent between versions, and in general it's
extremely buggy and poorly-written. So you might have to modify the
instructions slightly to get something that works.


### Aside: why software raid instead of MegaRAID?

Because the software that comes with LSI's RAID controllers is terrible. It's
called MegaCLI and you will never read anything good about it.

Examples of problems we've had in the past with MegaCLI:

* Random commands just don't work on some versions (but do work on others).
* Out of the ~5 versions we tried, all segfaulted on at least one of our
  physical servers, so we had to mantain two different versions of MegaCLI.
* It's ridiculously hard to use and lacking in documentation. The CLI design is
  junk. What does "RAID Level: Primary-1, Secondary-0, RAID Lvl Qualifier-0"
  mean without Googling it?
* Poor insight into drive health (can't just use smartctl/smartd), we had to
  write our own tools for it.
* No TRIM (needed for fast writes on our SSDs).

Plus, it's proprietary, which makes getting it installed automatically
difficult.

We are sacrificing a bit of measurable performance (mostly because we can't use
the battery-backed write cache), but we find it to be a small amount (and worth
the operational benefits of never having to touch MegaCLI again).


### Instructions

These assume you're willing to destroy all the data on the server and rebuild
it. They also assume you're currently using MegaRAID.

They work pretty reliably but you should still think before pressing enter,
because they might need some adjustment.

1. On boot, enter the LSI pre-boot CLI (press `Ctrl-Y` at the right time). The
   syntax in the pre-boot CLI seems to be the same as MegaCLI.

2. Remove all logical drives and put the physical drives in JBOD mode:

       $ -CfgLdDel -LALL -aALL
       $ -PDMakeGood -PhysDrv[252:0,252:1,252:2,252:3] -force -a0
       $ -AdpSetProp EnableJBOD 1 -aALL
       $ -PDMakeJBOD -PhysDrv[252:0,252:1,252:2,252:3] -a0
*note: I got an error on jaws on the `PDMakeJBOD`, but it worked anyway*

3. Reboot into finnix and figure out which drives you want in the RAID.

4. Make new partition tables on each drive and one large partition to hold the
   data.

   You should make the data partition take almost all of the space on the
   drive, but not all the way to the end (leave a GB or two). The reason is so
   that you can replace the drive when it fails with another drive which isn't
   quite the same size (it might be a few bytes smaller).

   ```bash
   for device in /dev/sda /dev/sdb /dev/sdc /dev/sdd; do
       parted "$device" mklabel gpt
       parted "$device" mkpart primary 10MB 510GB
   done
   ```

5. Pick one disk to hold GRUB (I usually do `/dev/sda`) and do:

   ```bash
   parted /dev/sda mkpart primary ext4 1 5
   parted /dev/sda
   ```

   Figure out the new partition number, then

   ```bash
   parted /dev/sda set 2 bios_grub on
   ```

6. Set up RAID 10, and make sure to use the data partitions (like `/dev/sda1`
   and not the entire drive).

   ```bash
   mdadm --create -v /dev/md0 --level=raid10 --raid-devices=4 \
       /dev/sda1 /dev/sdb1 /dev/sdc1 /dev/sdd1
   ```

7. Set up a GPT partition table on the new RAID volume. **Don't forget this or
   you'll be sorry when you have to abandon the Debian install.**

   ```bash
   parted /dev/md0 mklabel gpt
   ```

8. On `pestilence` (the DHCP server), you have to:

   * `systemctl disable puppet && systemctl stop puppet`
   * edit /etc/dhcp/dhcpd.conf and comment out the line that looks like:

         filename "http://contrib.ocf.berkeley.edu/preseed.cfg";

   * `systemctl restart isc-dhcp-server`

7. Back in Finnix, run `sync`.

8. Reboot and launch debian installer.

9. Make sure not to "OFC Automated Install" at PXE, do a manual install
   instead. sorry.

10. When you get to partitioning, use common sense. I recommend switching to
    another TTY and using fdisk to create ~30GB root, ~8GB swap, rest as one
    partition (for LVM). These should be created on `/dev/md0`.

11. When asked, install GRUB on the same disk as step 5 (I recommend /dev/sda).

12. When done, boot into WebCLI (`Ctrl-H` on boot at the LSI screen)

13. In WebCLI, figure out which disk you added your boot to, and set it as
    bootable. If you can't find the "Make Bootable" option on the physical
    drive page, it's probably already bootable. Maybe just restart and see if
    it works.

    I can't find a way to match drive letters inside webcli, so you might just
    need to try all of them in your new array until it works, sorry.

14. Undo everything from step 8 on `pestilence`.
15. You're done!
