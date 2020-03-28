[[!meta title="Using Twitch and OBS"]]

## Setting Up Your Stream

In your settings on Twitch, please enable VODs (video on demand) especially if you're working on OCF stuff.
To do this, go to https://dashboard.twitch.tv/settings/channel and enable "Store past broadcasts".

When streaming, keep the stream manager open (ideally on another screen) to see chat: https://dashboard.twitch.tv/stream-manager.

## Setting up OBS to stream to Twitch

OBS is pretty straightforward to configure. You can install it as you would any other software (arch pkg: obs-studio).

Please record on OBS as well streaming! (Click both the "Start Streaming" and "Start Recording" buttons.)
This will let us upload the streams to another source like YouTube. Twitch only saves VODs for a short period of time
It's recommended to set up at least two scenes in OBS: one that shows your desktop and one that does not. This way, you can hide your screen if you need to work with passwords or otherwise sensitive stuff. Keep in mind that "it only showed for a split second" is not an excuse to not hide things. Twitch allows people to clip and rewatch anything frame-by-frame.

Please stream with a mic so you can explain what you're doing and talk to chat. You can see the mic level in OBS. Ideally this should be hovering around the yellow range, but it should never hit the far right of the bar. If you're maxing out, decrease the mic volume. You can apply filters to the mic by clicking the gear icon.

I (cooperc) would recommend adding Noise Supression (reduces noise) and Noise Gate (cuts off all sound below a certain volume level). For Noise Gate, to set the thresholds, be quiet and see where the mic level ends up. Set the close threshold there, and set the open threshold 10dB higher.

If you know what a compressor is, you can add one as well. (Not like gzip or mp3 you nerds. Audio compression means something entirely different.)

## Screencasting in Arch on Wayland GNOME

(Note: this uses xdg-desktop-portal, which is currently only stable for GNOME, but is in development for wlroots (sway) https://github.com/emersion/xdg-desktop-portal-wlr and KDE)

- Install OBS: community/obs-studio
- Install desktop portal: extra/xdg-desktop-portal, extra/xdg-desktop-portal-gtk
- Install OBS plugin: aur/obs-xdg-portal-git

In OBS, add the "Desktop Screencast (Wayland/X11)" source to your scene.

**Note**: this setup uses pipewire, which recently upgraded to 0.3. If you're having issues, check to see if the file "/etc/pipewire/pipewire.conf.pacnew" exists.
If so, move this file to overwrite your old "/etc/pipewire/pipewire.conf"
