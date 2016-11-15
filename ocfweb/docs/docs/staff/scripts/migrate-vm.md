[[!meta title="migrate-vm: migrate VMs between hosts"]]

## Usage

This script is used for migrating [KVM virtual machines][kvm] between physical
hosts. The script should be run on the new host for the virtual machine using
the following format. The first hostname specified in the command is what
physical host to move the virtual machine from, and the second one is the name
of the virtual machine to move.

For example, the following command moves `supernova` from `jaws` to whatever
KVM host the command is run on:

    sudo migrate-vm jaws:supernova

[kvm]: https://wiki.debian.org/KVM

## Steps performed

To move the virtual machine, `migrate-vm` performs the following steps:

1. Shuts down the virtual machine on the old host.
2. Creates a new [LVM][lvm] volume on the new host with the correct size.
3. Securely copies the virtual machine's disk from the old host to the new
   host.
4. Checksums both the old and the new disks on each machine to ensure they
   match.
5. Imports the KVM domain definition from the old host to the new host.

[lvm]: https://wiki.debian.org/LVM

## Final steps

After the virtual machine has been transferred between hosts, make sure the
guest works on the new host. If moving from `hal`, you might need to delete the
custom CPU definition section from the KVM XML to get the virtual machine to
start. To edit the XML definition, run `sudo virsh edit ${hostname}`. The
section to delete looks like this:

```xml
<cpu mode='custom' match='exact'>
  <model fallback='allow'>Opteron_G3</model>
</cpu>
```

Then, after everything works, you should remove the old KVM and LVM definitions
on only the **old** host:

    sudo virsh undefine ${hostname}
    sudo lvremove /dev/vg/${hostname}

## Assumptions Made

- The LVM volume group `/dev/vg` is used on both the old and new host.
- Virtual machines are stored at `/dev/vg/${hostname}` on both hosts.
