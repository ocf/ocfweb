[[!meta title="Live disk resizing"]]

## Assumptions
1. You are resizing the disk to be a **larger** size than it currently is. If
   you would like to resize a disk to be smaller, that is much more complicated
   and will almost certainly require some downtime of the VM being resized.
2. This is being run on a KVM-based hypervisor with a locally-stored VM disk in
   LVM that's under `/dev/vg/<vm>`. If this is not the case, these commands may
   not work (mostly the ones under prerequisites, the later commands will
   likely still be fine)
3. The primary disk is the one being resized and it is located at `/dev/vda`.
   If a non-boot disk is being resized, it's likely going to be even easier
   than this guide says (probably no need to move swap), but otherwise a lot of
   the same steps will apply.

## Prerequisites

### On the KVM hypervisor

Resize the logical volume containing the VM's disk to increase by some number
of GiB. This assumes the path for the LVM-backed disk is in `/dev/vg/<vm>` but
it may be in a different directory within `/dev` depending on the volume group
name:

    $ export VM=<vm name here>
    $ sudo lvresize -L +<size in GiB>G /dev/vg/$VM

Get the new size in bytes for the disk (25 GiB here for instance):

    $ sudo fdisk -l /dev/vg/$VM | head -n 1
    Disk /dev/vm/<vm>: 25 GiB, 26843545600 bytes, 52428800 sectors

Resize the block device in `virsh` using the previous size in bytes:

    $ sudo virsh blockresize $VM /dev/vg/$VM <size in bytes>B

### On the VM (KVM guest)

The new disk size should have been detected by the kernel toward the bottom of
`dmesg` output:

    $ sudo dmesg | less
    [...]
    virtio_blk virtio1: [vda] new size: 52428800 512-byte logical blocks (26.9 GB/25.0 GiB)
    vda: detected capacity change from 21474836480 to 26843545600

Get some information about the disk (current partition sizes, types, current
disk size) before proceeding further. This can be useful to have in scrollback:

    $ sudo fdisk -l /dev/vda

If the disk is large enough (with partitions greater than 2 terabytes), then
`fdisk` might not work and it'll have to use GPT instead and be resized using
`parted`, but it's a similar process either way and both are detailed below.
Alternatively you can use `gdisk`, but that is not documented here yet or
installed on most hosts.

Turn swap off before proceeding further too since it will likely be moving.
The swap partition only needs to be moved if it's in the way of the expanding
partition, so if it's positioned before it (earlier on in the `fdisk` output
given above) then it won't need to be disabled, removed, and recreated and you
can skip turning it off here.

    $ sudo swapoff -a


## Method 1: `fdisk` (most common)

This is the path that uses `fdisk` to move partitions around. It's more common
to use, but if you need GPT support then you'll have to use `parted` below in
method 2. Note that `fdisk` will not write out any changes unless you give it
the `w` command to write them, so anything done up until that point should be
safe and you can exit without changes if it's not looking like you want it to.

    $ sudo fdisk /dev/vda

First, print out some information so you know what you are looking at. For
instance, this output shows a 25 GiB disk with a 18 GiB partition followed by a
~ 2 GiB extended partition containing some swap space. Note that the disk size
should be larger than all its contained partitions since you have just
increased its size previously:

    Command (m for help): p
    Disk /dev/vda: 25 GiB, 26843545600 bytes, 52428800 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0x29f3dc9e

    Device     Boot    Start      End  Sectors Size Id Type
    /dev/vda1  *        2048 37750783 37748736  18G 83 Linux
    /dev/vda2       37752830 41940991  4188162   2G  5 Extended
    /dev/vda5       37752832 41940991  4188160   2G 82 Linux swap / Solaris

Delete all current partitions (5 here is swap, 2 is extended partition, 1 is
root partition) since you'll be resizing the first one and moving the others
after it:

    Command (m for help): d
    Partition number (1,2,5, default 5): 5
    Partition 5 has been deleted.

    Command (m for help): d
    Partition number (1,2, default 2): 2
    Partition 2 has been deleted.

    Command (m for help): d
    Selected partition 1
    Partition 1 has been deleted.

Print out information (all partitions are deleted, at least in memory, but
nothing has been written yet):

    Command (m for help): p
    Disk /dev/vda: 25 GiB, 26843545600 bytes, 52428800 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0x29f3dc9e

Create a new root partition at partition 1. If you are asked about removing
signatures during this I usually just keep them around as none of the data or
flags should need changing and you are just growing the end of the partition:

    Command (m for help): n
    Partition type
       p   primary (0 primary, 0 extended, 4 free)
       e   extended (container for logical partitions)
    Select (default p):
    Partition number (1-4, default 1):
    First sector (2048-52428799, default 2048):
    Last sector, +sectors or +size{K,M,G,T,P} (2048-52428799, default 52428799): +24G

    Created a new partition 1 of type 'Linux' and of size 24 GiB.
    Partition #1 contains a ext4 signature.

    Do you want to remove the signature? [Y]es/[N]o: N

Create new swap partition with the remaining size (I didn't create an extended
partition, but feel free to if you'd like. It isn't really useful for most of
our VMs, it's only to get around a 4 partition limit on traditional partition
tables):

    Command (m for help): n
    Partition type
       p   primary (1 primary, 0 extended, 3 free)
       e   extended (container for logical partitions)
    Select (default p):
    Partition number (2-4, default 2):
    First sector (50333696-52428799, default 50333696):
    Last sector, +sectors or +size{K,M,G,T,P} (50333696-52428799, default 52428799):

    Created a new partition 2 of type 'Linux' and of size 1023 MiB.

Change the type of the new partition to be the correct type for swap (code 82):

    Command (m for help): t
    Partition number (1,2, default 2): 2
    Hex code (type L to list all codes): 82

    Changed type of partition 'Linux' to 'Linux swap / Solaris'.

You can set the bootable flag on the first partition if you'd like to match the
existing configuration, but it shouldn't matter on Linux as it's a setting that
only exists in the MBR for certain legacy clients:

    Command (m for help): a
    Partition number (1,2, default 2): 1

    The bootable flag on partition 1 is enabled now.

Print out data one last time before actually committing it:

    Command (m for help): p
    Disk /dev/vda: 25 GiB, 26843545600 bytes, 52428800 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0x29f3dc9e

    Device     Boot    Start      End  Sectors  Size Id Type
    /dev/vda1           2048 50333695 50331648   24G 83 Linux
    /dev/vda2       50333696 52428799  2095104 1023M 82 Linux swap / Solaris

**!! DANGER: Write the changes to the partition table !!**:

    Command (m for help): w
    The partition table has been altered.

If you see this error upon doing so, it can be safely ignored as you're going
to address this in the conclusion section:

    Calling ioctl() to re-read partition table.
    Re-reading the partition table failed.: Device or resource busy
    The kernel still uses the old table. The new table will be used at the next
    reboot or after you run partprobe(8) or kpartx(8).

Exit `fdisk` and continue to the conclusion section below.


## Method 2: `parted` (less common)

This is primarily useful for working with disks that have partitions over 2 TiB
in size and are using GPT (mirrors for instance when it was a VM), but it can
be used with smaller disks/partitions or non-GPT too. There's also a graphical
version at `gparted` if you have that option, but this does not assume you have
a graphical interface to work with.

**MAJOR WARNING**: When using `parted`, any changes you make are written out
immediately after making them, so you will not have the same opportunity to
review changes at the end as with `fdisk`!

Start off by entering `parted` and setting your units to use sectors (generally
more useful than bytes since you usually want to align partitions to sector
boundaries):

    $ sudo parted /dev/vda
    GNU Parted 3.2
    Using /dev/vda
    Welcome to GNU Parted! Type 'help' to view a list of commands.
    (parted) unit s

Then, print out the current settings. These are important to keep noted
somewhere as after you start removing partitions you cannot easily get this
information back:

    (parted) p
    Model: Virtio Block Device (virtblk)
    Disk /dev/vda: 54525952s
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos
    Disk Flags:

    Number  Start      End        Size       Type      File system     Flags
     1      2048s      50333695s  50331648s  primary   ext4            boot
     2      50333696s  52428799s  2095104s   extended
     5      50335744s  52428799s  2093056s   logical   linux-swap(v1)

If working with a GPT, you may get this prompt when printing the existing
partition information and need to fix the GPT to use all the space:

    Warning: Not all of the space available to /dev/vda appears to be used, you
    can fix the GPT to use all of the space (an extra 2147483648 blocks) or
    continue with the current setting?

    Fix/Ignore? Fix

Remove the old partitions, and go past a couple scary warnings for the root
partition that is in use. These can be ignored as we are going to fix this
later with `partprobe` and because no data is actually moving around:

    (parted) rm 5
    (parted) rm 2
    (parted) rm 1
    Warning: Partition /dev/vda1 is being used. Are you sure you want to continue?
    Yes/No? Yes

    Error: Partition(s) 1 on /dev/vda have been written, but we have been unable to
    inform the kernel of the change, probably because it/they are in use. As a result,
    the old partition(s) will remain in use.  You should reboot now before making
    further changes.
    Ignore/Cancel? Ignore

Create the partition again with the same starting value as before (2048s in
this case) and a larger ending value. The starting value here is crucial to get
the same as the previous one so that no data is shifted but the ending value
can be anything as long as it's greater than or equal to what it was before.
The units also do not have to match:

    (parted) mkpart primary 2048s 25GiB

Make a partition for swap (if you removed it before). You don't have to make an
extended partition, that's only there to make it so you can have more than 4
partitions total. `-1s` is used here to specify the last sector to use the
whole disk:

    (parted) mkpart primary linux-swap(v1) 25GiB -1s

Print the values again to make sure all looks good. Feel free to change units
to make sure things look good in GiB too. You're mostly looking to make sure
that the start of the main partition is the same as before, that it's larger
than before, and that no data except a swap partition had its start moved:

    (parted) p
    Model: Virtio Block Device (virtblk)
    Disk /dev/vda: 54525952s
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos
    Disk Flags:

    Number  Start      End        Size       Type     File system     Flags
     1      2048s      52428799s  52426752s  primary                  lba
     2      52428800s  54525951s  2097152s   primary  linux-swap(v1)  lba

    (parted) unit GiB
    (parted) p
    Model: Virtio Block Device (virtblk)
    Disk /dev/vda: 26.0GiB
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos
    Disk Flags:

    Number  Start    End      Size     Type     File system     Flags
     1      0.00GiB  25.0GiB  25.0GiB  primary                  lba
     2      25.0GiB  26.0GiB  1.00GiB  primary  linux-swap(v1)  lba

If you're using GPT, the first primary partition should have the `bios_grub`
flag set. The file systems shown shouldn't really matter here.

Quit `parted`. The values are already changed, so no saving is needed:

    (parted) quit

This will be shown, but we'll address this in the next steps below for the swap
partition if you had to move that:

    Information: You may need to update /etc/fstab.


## Conclusion (for either method used above):

### Let the kernel know that the partitions have changed

Run `partprobe` to start using the new partition table in the kernel without a
reboot:

    $ sudo partprobe

Magic!

### Resize the filesystem

`fdisk -l` should now show all the new information and partition sizes:

    $ sudo fdisk -l

Resize the filesystem to take up all of the partition's space:

    $ sudo resize2fs /dev/vda1
    resize2fs 1.44.5 (15-Dec-2018)
    Filesystem at /dev/vda1 is mounted on /; on-line resizing required
    old_desc_blocks = 2, new_desc_blocks = 2
    The filesystem on /dev/vda1 is now 6553344 (4k) blocks long.

`df -h` should show the correct new size now:

    $ df -h | grep /dev/vda1
    /dev/vda1        25G   15G  9.3G  61% /


### Re-create and re-enable swap

If you had swap on initially, re-create the swap area in the disk swap
partition (likely `/dev/vda5` if you have the extended partition and
`/dev/vda2` if you do not):

    $ sudo mkswap /dev/vda2
    Setting up swapspace version 1, size = 1022 MiB (1071640576 bytes)
    no label, UUID=4eb9847b-3028-4b0a-8a34-f38373c9edd8

Update the swap device UUID (the one with `swap` and `sw` in its line) in
`/etc/fstab` with the new one printed out by `mkswap` in the previous step:

    $ sudo vim /etc/fstab

Finally, turn swap back on:

    $ sudo swapon -a
