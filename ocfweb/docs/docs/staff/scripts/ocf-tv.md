[[!meta title="ocf-tv: connect to the tv or modify the volume"]]

The usage of `ocf-tv` looks like:

    ocf-tv [-h] [-H HOST] {connect,volume,mute,stop-tunnel,tunnel-audio}

If you provide no arguments to `ocf-tv` the default behavior is that it will
start a VNC session to the TV. If you do not specify the host it will use the
TV by default.

`ocf-tv connect` will open up a VNC window using `xvncviewer` to the host.
The TV uses [[i3wm|doc staff/i3wm]], a tiling window manager, so if you are
unsure of how to use it read the linked documentation.

If you'd like to just change the volume on the host, you can use the
`volume` or `mute` options to change the pulseaudio volume level.
`ocf-tv volume 50` sets the remote volume to 50% (acceptable values in [0,150])
and `mute` does what you might expect.

If you'd like to tunnel audio playing on your local desktop to the TV (for
example, so you don't have to manipulate YouTube over VNC), you can start
the tunnel via `ocf-tv tunnel-audio` from any desktop, and similarly, use
`ocf-tv stop-tunnel` to close the tunnel and resume local-only playback.
