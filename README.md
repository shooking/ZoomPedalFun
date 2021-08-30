# ZoomPedalFun
A collection of tips and tricks for Zoom B1On, B1XFour and G1XFour pedals.

The aim of this work is to allow others to trial any tips & tricks found, at their own risk, to get more fun out of these wonderful pedals.

If you want to contribute then hit me up in the issues (technical not financial!).

I also draw you attention to other great works in this area:

(B1ON) zoom Effect Manager: https://www.reddit.com/r/zoommultistomp/comments/jcjk04/new_zoom_effect_manager_111/

Barsik-Barbosik Zoom Firmware Editor: https://github.com/Barsik-Barbosik/Zoom-Firmware-Editor

Mungewell's Zoom-zt2: https://github.com/mungewell/zoom-zt2

SysExTones g1on: https://github.com/SysExTones/g1on

SrMouraSilva: https://github.com/PedalController/PiPedalController

ZDownload: https://github.com/fuzboxz/zdownload

Zoom-dev midi docs: https://github.com/zoom-dev/MIDIDocs

Decent editors:

ToneLib: https://tonelib.net/

Offical pages:

Zoom: https://www.zoom.co.jp/products/effects-preamps/guitar

AIMS

To provide a variety of scripts, along with some supplementary YouTube content (see https://www.youtube.com/user/stephenhookings1985 playlist Miscellaneous Guitar Tools and Mods) that allow folks to get more out of their pedals. This is shared as Creative Commons - share and share alike.

If you know of some tricks and tips and would like to share them, open up an Issue and we can explore how to merge the content.

RECOMMENDED HARDWARE

You will likely need a Windows PC or Mac for some activities.
But this is only if you want to brew everything yourself.

Most of my experiments require a Raspberry Pi 4 (3 would probably do).
A Linux box would also likely work.
A Linux box under a VM does not work so well - the USB passthru confuses the device names.

Why the Pi?
It is cheap, so should not be too great an entry barrier.
It has GPIO pins should we want to create external controls.
It is near silent, small and supports a range of touchscreens.
I ported Ctrlr to run on it - so it becomes a viable controller platform.
I would have used Andrid tablets but I never found these to be as versatile.
It supports a range of programming toolchains.
I love Linux type OS's.
etc etc.

What Languages will you use?

Initially Bash scripts. Because all the main Linux's have this.
And learning bash is a decent skill in any case.

For reverse engineering I tend to use Python and WireShark/PCAP.
MidiOX can be useful on a Windows box.

I will also be using C/C++ for some activities just because it is so quick.

For Ctrlr we are forced (not in a bad way) to use Lua.

What do you want to get out of this Steve?

To share some useful tips and tricks with fellow musicians about how cool these Zoom pedals are.
I am not affiliated with Zoom, nor sponsored. Ideally if they would open up their Sysex (as per Dave Smith's original aim for Midi) that would be cool - it would save me a ton of time.
And it would create new markets for their products. So it you like this is a small amount of pressure to respectfully ask Zoom to be more transparent.

As it stands their products are generally exception value for money and for sure I would buy again from them if my pedal broke.

It would be cool to meet and collaborate with like minded people across our planet.
I open this NOT as competition with Mungewell but as a collaborative effort.
He prefers to keep C++ away from his work - no problems. And you see I added some content to his work.
And we both stand on the shoulders of Barsik.

Also this sort of work stops me going stir crazy during lockdown. I hope anyone reading is doing ok.
If you need some stress release - break out your bass, guitar or even synth with one of these Zoom pedals.
It opens a lot of creative energy.

Thanks and looking forward to working with you.
Steve, Feb 2021.
