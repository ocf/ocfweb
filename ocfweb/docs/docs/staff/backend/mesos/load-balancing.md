[[!meta title="Load balancing"]]

## Common tasks and questions
### General
#### A service is unreachable, how do I troubleshoot?    {troubleshoot}

These are general steps:

1. Can you ping `lb.ocf.berkeley.edu`? If not, then most likely none of the
   three master servers are using that IP, and so `keepalived` is probably broken.

2. Find the currently keepalived host, then do `curl <host>:9090/_haproxy_getconfig`.
   If you get connection refused, then `marathon-lb` is probably broken. If you
   get back a bad config (missing backends or servers), probably Marathon is
   unhealthy (check the `marathon-lb` logs—they'll probably indicate they can't
   reach Marathon, or similar). If everything here looks good, move on.

3. Take one of the `server` entries from the previous step and try to curl it.
   For example, if you saw the line:

   ```haproxy
   server hal_169_229_226_10_31754 169.229.226.10:31754 check inter 60s fall 4
   ```

   You would do `curl 169.229.226.10:31754` and make sure you get a response.
   If you do, then move on. If not, it's most likely that `marathon-lb` has a
   different world-view than Marathon (maybe Marathon is unhealthy?). Check the
   logs.

4. Most likely at this stage, `nginx` is broken on the load balancers. Try to
   curl the load balancers on port 80 and 443, and check the nginx logs.


### keepalived    {keepalived}
#### How do I figure out who the current leader is?

You can do `ssh lb` and see what you get connected to, but will probably have
to deal with the key changing if you do this often.

TODO: is there a better way?


#### How do I force a leadership change (e.g. to perform maintenance)?

TODO: not sure


### marathon-lb    {marathon-lb}
#### How do I manage `marathon-lb` on some host?

`marathon-lb` is a systemd service running as `ocf-lb`.

* **Check the status.** `systemctl status ocf-lb`
* **Look at the logs.** `journalctl -eu ocf-lb`
* **Restart it.** `systemctl restart ocf-lb`


#### How do I see the current haproxy config on a host?

```bash
ckuehl@supernova:~$ curl mesos0:9090/_haproxy_getconfig
global
  daemon
  log /dev/log local0
  log /dev/log local1 notice
  maxconn 50000
[...]
```

If everything is working, you should see a backend for each app exposed on the
load balancer, with one or more servers in it. For example, here is a working
ocfweb backend with three servers:

```haproxy
backend ocfweb_web_10002
  balance roundrobin
  mode tcp
  server hal_169_229_226_10_31754 169.229.226.10:31754 check inter 60s fall 4
  server pandemic_169_229_226_14_31005 169.229.226.14:31005 check inter 60s fall 4
  server pandemic_169_229_226_14_31419 169.229.226.14:31419 check inter 60s fall 4
```


### mesos-dns
#### How do I see how `mesos-dns` is working on some host?

```bash
ckuehl@supernova:~$ dig leader.mesos @mesos1
[...]
;; QUESTION SECTION:
;leader.mesos.                  IN      A

;; ANSWER SECTION:
leader.mesos.           1       IN      A       169.229.226.52
[...]
```

To check against the main DNS server (and not the masters), just run the same
command with `@ns`.


#### How do I manage `mesos-dns` on some host?

`mesos-dns` is a systemd service.

* **Check the status.** `systemctl status mesos-dns`
* **Look at the logs.** `journalctl -eu mesos-dns`
* **Restart it.** `systemctl restart mesos-dns`
