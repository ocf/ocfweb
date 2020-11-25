[[!meta title="Using Twitch and OBS"]]

## Preparing Your Stream

In your settings on Twitch, please enable VODs (video on demand) especially if
you're working on OCF stuff. To do this, go to your [Twitch channel
settings](https://dashboard.twitch.tv/settings/channel) and enable "Store past
broadcasts". Note that VODs do not last forever (14 days for regular Twitch
users); see the recommendations section below on how to save your stream.

When streaming, keep the [Stream
Manager](https://dashboard.twitch.tv/stream-manager) open (ideally on another
screen) to see chat. You can get to this from
[https://dashboard.twitch.tv/stream-manager](https://dashboard.twitch.tv/stream-manager).

## Setting up OBS to stream to Twitch

OBS is pretty straightforward to configure. You can install OBS by following the
[official instructions here](https://obsproject.com/wiki/Install-Instructions),
and you can find additional guidance from the [OBS official wiki
here](https://obsproject.com/wiki/).

When you first open OBS, you'll encounter a first-time setup screen. Be sure to
run through the options and make sure to optimize for streaming over recording.

OBS operates by providing **sources** (input from your computer and connected
devices) that you can assemble into custom arrangements called a **scene**. We
recommend setting up at least two scenes in OBS: one that shows your desktop and
one that does not. This way, you can hide your screen if you need to work with
passwords or otherwise sensitive stuff. You can switch streams by clicking on
the scene on OBS or assigning hotkeys to each scene.

A beginning setup could look like the following:

1. Scene 1 ("Normal")
  - Audio Input Capture (microphones, etc)
  - Audio Output Capture (streams audio from the computer)
  - Screen Capture (screen capture)
  - Video Capture Device (webcams -- optional)
2. Scene 2 ("Desktop Hidden")
  - Picture
  - Text ("Be right back!")

Once you've configured everything properly and connected OBS to Twitch, press
"Start Streaming" to begin streaming to Twitch.

## Streaming Reminders & Recommendations

- Please record on OBS while streaming! Click both the "Start Streaming" and
  "Start Recording" buttons. This will allow you to upload the streams to
  another source like YouTube. Twitch only saves VODs for a short period of
  time.

- We advise streamers to **be very careful about what they show on screen**;
  Twitch allows people to clip and rewatch anything frame-by-frame.

- Please stream with a mic so you can explain what you're doing and talk to
  chat. You can see the mic level in OBS. Ideally this should be hovering around
  the yellow range, but it should never hit the far right of the bar. If you're
  maxing out, decrease the mic volume. You can apply filters to the mic by
  clicking the gear icon.

- OBS has several options that will optimize stream quality. If you have a
  powerful discrete GPU, enable video hardware encoding through your GPU.

- We recommend adding Noise Suppression (reduces noise) and Noise Gate (cuts off
  all sound below a certain volume level). For Noise Gate, to set the
  thresholds, be quiet and see where the mic level ends up. Set the close
  threshold there, and set the open threshold 10dB higher.

- If you know what a
  [compressor](https://en.wikipedia.org/wiki/Dynamic_range_compression) is, you
  can add one as well. (Not recommended if you aren't familiar.)

## Screencasting in Arch on Wayland GNOME

(Note: this uses xdg-desktop-portal, which is currently only stable for GNOME,
but is in development for wlroots (sway)
https://github.com/emersion/xdg-desktop-portal-wlr and KDE)

- Install Wayland OBS: aur/obs-studio-wayland
- Install desktop portal: extra/xdg-desktop-portal, extra/xdg-desktop-portal-gtk
- Install OBS plugin: aur/obs-xdg-portal-git

Start OBS with the environment variable `QT_QPA_PLATFORM=wayland` to
make sure it runs in Wayland instead of XWayland.

In OBS, add the "Desktop Screencast (Wayland/X11)" source to your scene.

**Note**: this setup uses pipewire, which recently upgraded to 0.3. If you're
having issues, check to see if the file "/etc/pipewire/pipewire.conf.pacnew"
exists.  If so, move this file to overwrite your old
"/etc/pipewire/pipewire.conf"
