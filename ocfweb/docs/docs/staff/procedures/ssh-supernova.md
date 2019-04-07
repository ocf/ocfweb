[[!meta title="SSHing into Supernova"]]

When contributing to the OCF codebase, you will need some way of running and
testing your code. Most of our applications cannot be run on a personal
machine--they need to be run on OCF infrastructure. For most projects we
recommend doing all development from `supernova`, a server available to all
staff. Our [[Kubernetes server|doc staff/backend/kubernetes]] is also
accessible from `supernova`.

## Before you begin
You need to be on staff to log into the server. If you're not sure whether or
not you're on staff, try logging in. If this doesn't work, talk to a staff
member and we can add you! All are welcome and encouraged to join.

## Logging in
To log in, open a terminal window and type in:

```
ssh username@supernova.ocf.berkeley.edu
```

For more instructions, see the [[SSH docs|doc services/shell]]. You should
replace `ssh.ocf.berkeley.edu` with `supernova.ocf.berkeley.edu`.

## Things you can do on `supernova`

### Administration scripts

Some scripts, such as ones used to create group accounts and refund printing
quotas, are available on `supernova`. Learn more about these in the scripts
section of [[staff documentation|doc staff]].

### Development and Testing
You can `git clone` OCF repositories and run them on `supernova`. An example
for `ocfweb`:

```
git clone https://github.com/ocf/ocfweb # clone the repository
cd ocfweb # change directory into the repository

... make changes ...

make test # run tests to make sure everything is working
make dev # start a development server and see your changes live
```

### Kubernetes
To access Kubernetes, simply run `kubectl` commands. See the [Kubernetes
documentation][kubernetes-basics] for more information.

[kubernetes-basics]: https://kubernetes.io/docs/tutorials/kubernetes-basics/
