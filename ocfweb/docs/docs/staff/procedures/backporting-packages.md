[[!meta title="Backporting packages"]]

It seems like we often either need a newer version of a package, or to apply
our own patch to some package. We have [an apt
repo](http://apt.ocf.berkeley.edu/) to which we upload these packages.

There is a useful Debian wiki page
[SimpleBackportCreation](https://wiki.debian.org/SimpleBackportCreation) but
we'll cover everything you need to know here.

## Step 1: Find the package you want

* Go to [packages.debian.org](https://packages.debian.org/) and find the
  package you desire.

* Find the package info page
  ([example](https://packages.debian.org/stretch/evince)), and make sure you're
  on the correct distribution (select at the top-right, e.g. `stretch`).

* From the sidebar on the right, select under "Download Source Package" the
  link to the `.dsc` file. The URL should look something like:

      http://http.debian.net/debian/pool/main/e/evince/evince_3.14.2-1.dsc


## Step 2: Downloading the package

* Log on to a system which has the release you want to eventually install the
  package on. (If you're backporting a package from stretch to jessie, you
  should do these steps *on jessie*.)

* Using the `.dsc` link from above, download the source package:

      dget -x http://http.debian.net/debian/pool/main/e/evince/evince_3.14.2-1.dsc


## Step 3: Install dependencies

* Enter the new directory and run `dpkg-checkbuilddeps`, and install any
  dependencies that are missing. If you'd like to install missing
  dependencies automatically, you can use `sudo mk-build-deps -i`.


## Step 4: Make any changes (optional)

If you're patching the package (and not just backporting), here is where you
make your changes. You should first apply all the patches (`dquilt push -a`),
then use quilt to create your patch. You can also just modify the source if you
don't care about quality, but you *should* ensure the Debian patches are
applied first.


## Step 5: Update the version number using dch

Decide on your version number, using one of the categories below:


### Backports

For backports, we like to add append `~ocfN` to the end, where `N` is an
integer starting at 1. The final version might look like `4.3.0-1~ocf1`.

Use a command like:

    dch --local ~ocf --distribution jessie-backports "Backported by OCF for jessie."

The squiggly makes your backport inferior to the official package, so that it
will be replaced during an upgrade. This is desired.

### Patched packages

For packages we apply patches to, we like to append `ocfN` to the end. This is
similar to what Ubuntu does. The final version might look like `1.3.1-7ocf1`.

Use a command like:

    dch --local ocf --distribution jessie "Patched by OCF to not recursively delete $HOME on login."


## Step 6: Build the package

* Test that you can build the package with `fakeroot debian/rules binary`. Fix
  any errors.

* Build the package with `dpkg-buildpackage -us -uc -b`. The `.deb` file will
  pop out in your parent directory.


## Step 7: Test and upload to our apt repo

If this is something that we will be building often (e.g. atool or ocflib), you
probably want to set it up inside Jenkins to automatically upload to apt.

For one-off uploads:

1. `scp` the file to fallingrocks
2. `sudo -u ocfapt /opt/apt/bin/reprepro includedeb jessie /tmp/mydeb.deb`

(For more options for `reprepro`, see the comments at the top of that file.)
