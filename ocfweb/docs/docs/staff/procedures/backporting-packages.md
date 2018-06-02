[[!meta title="Backporting Debian packages"]]

It seems like we often either need a newer version of a package, or to apply
our own patch to some package. We have [an apt
repo](http://apt.ocf.berkeley.edu/) to which we upload these packages.

There is a useful Debian wiki page
[SimpleBackportCreation](https://wiki.debian.org/SimpleBackportCreation) but
we'll cover everything you need to know here.

Additionally, some of the commands on this page are found in packages not
typically installed on OCF machines. In order of appearance on this page:

* `dget`: Found in the `devscripts` package
* `dpkg-checkbuilddeps`: Found in the `dpkg-dev` package
* `mk-build-deps`: Found in the `devscripts` package
* `dquilt`: This is [an alias around `quilt`][dquilt], found in the `quilt` package
* `dch`: Found in the `devscripts` package
* `dpkg-buildpackage`: Found in the `dpkg-dev` package
* `scp`: Found in the `openssh-client` package

Generally, it's a good idea to build packages in Docker containers so that any
build dependencies or build tools are not left still installed after the
package is built. In total, you only generally need to run:

    sudo apt install packaging-dev debian-keyring devscripts equivs openssh-client

to get started with building packages (`packaging-dev` installs a bunch of the
packages above as dependencies). This is along with any build dependencies the
packages you are working on might have, but this is discussed more later.

[dquilt]: https://www.debian.org/doc/manuals/maint-guide/modify.en.html#quiltrc

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
  package on. (For example, if you're backporting a package from buster to
  stretch, you should do these steps *on stretch*.) Generally, a Docker
  container works quite well because any extra build dependencies you install
  will not remain on the system once the package is built. pbuilder can also be
  used to a similar effect.

* Using the `.dsc` link from above, download the source package:

      dget -x http://http.debian.net/debian/pool/main/e/evince/evince_3.14.2-1.dsc


## Step 3: Install dependencies

* Enter the new directory and run `dpkg-checkbuilddeps`, and install any
  dependencies that are missing. If you'd like to install missing dependencies
  automatically, you can use `sudo mk-build-deps -ir`.


## Step 4: Make any changes (optional)

If you're patching the package (and not just backporting), here is where you
make your changes. You should first apply all the patches (`dquilt push -a`),
then use `dquilt`/`quilt` to create your patch. This can be done by running
`dquilt new <patch-name>.patch` to start a patch, `dquilt edit <file>`, and
then `dquilt refresh` to generate the patch file from the modified file. You
can also just modify the source if you don't care about quality, but you
*should* ensure all the Debian patches are applied first using `dquilt`.


## Step 5: Update the version number using dch

Decide on your version number, using one of the categories below:

### Backports

For backports, we like to add append `~ocfN` to the end, where `N` is an
integer starting at 1. The final version might look like `4.3.0-1~ocf1`.

Use a command like:

    dch --local ~ocf --distribution stretch-backports 'Backported by OCF for stretch.'

The squiggle makes your backport inferior to the official package, so that it
will be replaced during an upgrade. This is desired, since with a backport no
changes have been made to the package itself, just a newer version brought to
an older distribution version.

### Patched packages

For packages we apply patches to, we like to append `ocfN` to the end. This is
similar to what Ubuntu does for packages it patches from Debian. The final
version might look like `1.3.1-7ocf1`.

Use a command like:

    dch --local ocf --distribution stretch 'Patched by OCF to not delete $HOME on login.'

Unlike backporting, this version number means that upgrades will not affect this
package, since it will not be inferior to any new versions pushed to Debian
package repos. This is usually desired because the patch applied should not be
automatically overwritten by any other changes to the package.


## Step 6: Build the package

Build the package with `dpkg-buildpackage -us -uc -sa`. The `.deb` file will
pop out in your parent directory along with some other files to send to the apt
repo (the original source, any modifications, the changelog, etc.).


## Step 7: Upload to our apt repo and test

If this is something that we will be building often (e.g. ocfweb or ocflib),
you probably want to set it up inside Jenkins to automatically test and
[upload to apt](https://jenkins.ocf.berkeley.edu/job/upload-changes/).

For one-off uploads:

1. Copy all the necessary files to `apt` (currently `fallingrocks`):

       scp *.tar.gz *.tar.bz2 *.debian.tar.xz *.dsc *.changes *.deb you@apt:/tmp/yourpackage

   Generally putting these in a new directory in `/tmp` is a good way to go,
   since if you put them in your home directory, the `ocfapt` user will not be
   able to read them.

2. Include the package files in the suitable distribution. If this is just a
   backport (no patches), use `<dist>-backports`, otherwise just use `<dist>`:

       sudo -u ocfapt /opt/apt/bin/reprepro include <dist> /tmp/mypackage.changes

   For more options for `reprepro`, see the comments at the top of
   `/opt/apt/bin/reprepro`, which is a wrapper script around the `reprepro`
   command to avoid messing up paths and permissions.

3. Test the package by installing it on one host and see if it behaves how you
   would expect. Make sure to run `sudo apt update` first so that the host you
   are testing on knows about the package you have added.
