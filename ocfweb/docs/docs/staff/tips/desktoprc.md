[[!meta title=".desktoprc"]]

The file `~/remote/.desktoprc` is automatically sourced when you log into any
of the desktops. Since `~/remote` is actually `sshfs`'d to your home folder on
NFS, this means you can put your common config or preferences in it and have
them be shared across all desktops.

## Example uses

If you want to get a feel for what you can do with your `.desktoprc`, try out
some of these useful ideas.

### Sync your dotfiles

If you want your application settings shared between the desktops and login
servers, you can just copy them over with a line like this:

    cp ~/remote/{.bashrc, .bash_aliases, .vimrc, ...} ~/

Alternatively, if you have a [dotfile repo](https://dotfiles.github.io/), you
can either clone it...

    git clone https://github.com/username/dotfiles.git ~/.dotfiles
    ~/.dotfiles/my-install-script

... or just link to it in your NFS homedir, if you have it there:

    ln -s ~/remote/.dotfiles ~/.dotfiles
    ~/.dotfiles/my-install-script

### Configure HexChat (IRC)

We install HexChat as a desktop IRC client. You can automatically configure it
to connect to your favorite networks on startup. For example, to automatically
connect to the OCF's IRC server, try this snippet:

    mkdir -p ~/.config/hexchat
    echo "
    v=2.12.4

    N=ocf
    L=7
    E=UTF-8 (Unicode)
    F=30
    D=0
    S=irc.ocf.berkeley.edu/6697
    J=#rebuild
    " > ~/.config/hexchat/servlist.conf

For more complex configs, you always have the option to edit your server list
from the GUI, then copy and paste `servlist.conf` into your `.desktoprc`.

### Disable terminal shortcuts

The XFCE4 terminal emulator installed on the desktops comes with keyboard
shortcuts by default. If these bother you, you can disable them like this:

    echo "
    ShortcutsNoHelpkey=TRUE
    ShortcutsNoMenukey=TRUE
    ShortcutsNoMnemonics=TRUE
    " >> ~/.config/xfce4/terminal/terminalrc
