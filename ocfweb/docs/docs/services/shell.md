[[!meta title="Shell (SSH/SFTP)"]]

A shell account refers to a text-mode interface where commands can be run interactively. All OCF accounts include shell account access. You can access your shell account over an encrypted connection in the OCF lab or remotely via SSH/SFTP.

We support the following commonly used shell account tools (to name a few):

*   Subversion, Git, and Mercurial: version control
*   cron and at: execute commands on a periodic or scheduled basis
*   vim and emacs: powerful and extensible text editors

Most SSH/SFTP clients will prompt you to accept an unknown key when you first connect. Our SSH fingerprint can be used to verify that you're connecting to the correct server:

    2048 55:0a:e3:4f:4b:2c:15:f8:d4:7d:f9:93:bf:a0:41:21 tsunami.ocf.berkeley.edu (RSA)
    1024 7e:19:bc:fd:b5:cd:5c:e3:42:a4:a5:74:eb:ce:5d:2e tsunami.ocf.berkeley.edu (DSA)
    256  a2:4b:d5:17:43:2e:a7:ea:50:d7:ab:1f:63:45:a9:6c tsunami.ocf.berkeley.edu (ECDSA)
    256  SHA256:h6Rnqg1tyl6VMFrotrR+DSnNW6DF8wQylVllkp03DIw tsunami.ocf.berkeley.edu (ECDSA)

## SSH

Your shell account can be controlled remotely using [SSH](https://en.wikipedia.org/wiki/Secure_Shell). The server name is <tt>ssh.ocf.berkeley.edu</tt> (<tt>tsunami</tt>).

#### From your browser
If you just need to access SSH quickly, you can use our [web-based SSH interface](https://ssh.ocf.berkeley.edu/) from your web browser.

#### Mac OS X or Linux

On Mac OS X or Linux, enter in the terminal:

    ssh username@ssh.ocf.berkeley.edu

#### Windows
On Windows, use [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) (download the `putty.exe` file):

* Host Name: `ssh.ocf.berkeley.edu`
* Port: 22



## SFTP

You can transfer files to your account using [SFTP](https://en.wikipedia.org/wiki/SSH_File_Transfer_Protocol). To transfer files, you'll need another program, such as [FileZilla](https://filezilla-project.org/), [WinSCP](http://winscp.net/) (Windows), or [Cyberduck](https://cyberduck.io/) (Mac OS X, Windows).

Otherwise, use the following information in your SFTP client.

* Protocol: SFTP (or SSH)
* Host Name: `ssh.ocf.berkeley.edu`
* Port: 22
