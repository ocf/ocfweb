[[!meta title="ocf-tv: connect to the tv or modify the volume"]]

The usage of `ocf-tv` looks like:

    ocf-tv [-h] [--host HOST] {connect,volume,mute}

If you provide no arguments to `ocf-tv` the default behavior is that it will
connect to the TV. If you do not specify the host it will use the TV by default.

`ocf-tv` connect will open up a VNC window using `xvncviewer` to the host.
The TV uses [i3wm](doc staff/i3wm), a tiling window manager, so if you are
unsure of how to use it read the linked documentation.

If you'd like to just change to volume on the host, you can use the
`volume` or `mute` option to change the pulseaudio volume level.
`volume` takes a number in [0,150] and `mute` will just mute the host.
