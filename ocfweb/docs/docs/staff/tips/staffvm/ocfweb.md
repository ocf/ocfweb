[[!meta title="Running ocfweb"]]

If you want to work on [`ocfweb`][0] on your Staff VM, it isn't as
simple as cloning the repo and running `make dev`, unfortunately.
In order to do so, you will need to add the `ocfweb` dev config to
your Staff VM's Puppet configuration, so Puppet can install
`ocfweb`'s config files. To do this, clone the [puppet repo][1] or
go to `/opt/puppet/env/<you>` on `lightning`, and then in
`hieradata/nodes/` add the following lines to your staff VM's Hiera
configuration:

    classes:
        - ocf_ocfweb::dev_config

Take a look at the configs for [`fireball`][2] or [`raptors`][3] for
examples.

If you are in `ocfroot` you can push this directly to puppet and
trigger a puppet run on your staffvm (`sudo puppet-trigger -fe <user>`)
otherwise, push to your fork and submit a pull request and someone will
merge it for you, after which you can trigger the puppet run on your VM.

Furthermore, you will need to install the `libcrack2-dev` package so that
the crypto libraries `ocfweb` depends on will successfully compile.

[0]: https://github.com/ocf/ocfweb
[1]: https://github.com/ocf/puppet
[2]: https://github.com/ocf/puppet/blob/master/hieradata/nodes/fireball.yaml
[3]: https://github.com/ocf/puppet/blob/master/hieradata/nodes/raptors.yaml
