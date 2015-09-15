[[!meta title="Installing and Running ZNC"]]

Installing and running ZNC on your staff VM is easy and highly recommended.

## What is ZNC?

ZNC is an *IRC bouncer*. It keeps you always connected to IRC, and allows you
to connect to the bouncer from your desktop client, irssi, phone, etc.

It's handy to avoid constantly disconnecting/reconnecting from IRC. It will
also store messages you've missed and replay them when you log in.

It's useful along with [[OCF's IRC server|doc contact/irc]].

## Installing ZNC on your staff VM

1. `sudo apt-get install znc`

2. Create a config file for ZNC. As your user (i.e. not as root), run `znc
   --makeconf`. It's pretty safe to accept the defaults (just hit enter), but
   you'll probably want to enable webadmin.

   The settings I use (everything else I accept defaults):

       ckuehl@raptors:~$ znc --makeconf
       [ ?? ] What port would you like ZNC to listen on? (1025 to 65535): 4095

       [ ?? ] Would you like ZNC to listen using SSL? (yes/no) [no]: yes
       [ ?? ] Would you like ZNC to listen using both IPv4 and IPv6? (yes/no) [yes]: no

       [ ?? ] Load global module <webadmin>? (yes/no) [no]: yes

       [ ** ] Now we need to set up a user...
       [ ** ]
       [ ?? ] Username (AlphaNumeric): ckuehl
       [ ?? ] Enter Password:
       [ ?? ] Confirm Password:
       [ ?? ] Would you like this user to be an admin? (yes/no) [yes]: yes
       [ ?? ] Nick [ckuehl]:
       [ ?? ] Alt Nick [ckuehl_]:
       [ ?? ] Ident [ckuehl]:
       [ ?? ] Real Name [Got ZNC?]: Chris Kuehl

       [ ?? ] Load module <chansaver>? (yes/no) [no]: yes
       [ ?? ] Load module <controlpanel>? (yes/no) [no]: yes
       [ ?? ] Load module <perform>? (yes/no) [no]:
       [ ?? ] Load module <webadmin>? (yes/no) [no]: yes

       [ ?? ] Would you like to set up a network? (yes/no) [no]: yes
       [ ?? ] Network (e.g. `freenode' or `efnet'): ocf

       [ ?? ] Load module <chansaver>? (yes/no) [no]: yes
       [ ?? ] Load module <keepnick>? (yes/no) [no]: yes

       [ ** ] -- IRC Servers --
       [ ** ] Only add servers from the same IRC network.
       [ ** ] If a server from the list can't be reached, another server will be used.
       [ ** ]
       [ ?? ] IRC server (host only): irc.ocf.berkeley.edu
       [ ?? ] [irc.ocf.berkeley.edu] Port (1 to 65535) [6667]: 6697
       [ ?? ] [irc.ocf.berkeley.edu] Password (probably empty):
       [ ?? ] Does this server use SSL? (yes/no) [no]: yes

       [ ?? ] Would you like to add a channel for ZNC to automatically join? [yes]: yes
       [ ?? ] Channel name: #rebuild
       [ ?? ] Would you like to add another channel? (yes/no) [no]: yes
       [ ?? ] Channel name: #ocf

       [ ?? ] Launch ZNC now? (yes/no) [yes]: no

3. If you accidentally started ZNC at the end of the setup, you should kill it
   now with `pkill znc`.

4. Now we'll set up systemd to supervise ZNC for us.

   Create a file `/lib/systemd/system/znc.service` with the contents:

       [Unit]
       Description=znc

       [Service]
       User=<YOUR_USER>
       ExecStart=/usr/bin/znc --foreground
       Restart=always

       [Install]
       WantedBy=multi-user.target

   Make sure to change `<YOUR_USER>` to your username!

5. Reload systemd and start znc:

    * `systemctl daemon-reload`
    * `systemctl enable znc`
    * `systemctl start znc`

ZNC should now be running (and will start/restart automatically). You can see
detailed information with `systemctl status znc`.

If you enabled webadmin, you can access your server at
`https://<your_staff_VM>.ocf.berkeley.edu:PORT/`. Make sure you use `https` or
you'll get a cryptic "connection reset" message.
