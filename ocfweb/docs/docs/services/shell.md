[[!meta title="Remote shell and file transfer (SSH/SFTP)"]]

A shell account refers to a text-mode interface where commands can be run
interactively. All OCF accounts include shell account access. You can access
your shell account over an encrypted connection in the OCF lab or remotely via
SSH/SFTP.

We support the following commonly used shell account tools (to name a few):

*   Subversion, Git, and Mercurial: version control
*   cron and at: execute commands on a periodic or scheduled basis
*   vim and emacs: powerful and extensible text editors

Most SSH/SFTP clients will prompt you to accept an unknown key when you first
connect. Our SSH fingerprint can be used to verify that you're connecting to
the correct server:

    1024 SHA256:xz0N4OqJtabwVvdAy6AvmXSG/Ct1cVyoSv7Ag75eYg8  tsunami.ocf.berkeley.edu (DSA)
    1024 MD5:7e:19:bc:fd:b5:cd:5c:e3:42:a4:a5:74:eb:ce:5d:2e tsunami.ocf.berkeley.edu (DSA)
    256  SHA256:h6Rnqg1tyl6VMFrotrR+DSnNW6DF8wQylVllkp03DIw  tsunami.ocf.berkeley.edu (ECDSA)
    256  MD5:a2:4b:d5:17:43:2e:a7:ea:50:d7:ab:1f:63:45:a9:6c tsunami.ocf.berkeley.edu (ECDSA)
    256  SHA256:queQQ1NML1znAVQTaYirF/R5WKEVSAPnRXjEVQug7Xw  tsunami.ocf.berkeley.edu (ED25519)
    256  MD5:c6:dc:62:4f:51:8b:b1:c3:72:cf:d4:63:65:92:6f:2d tsunami.ocf.berkeley.edu (ED25519)
    2048 SHA256:X5sl/Pw8Knjl4evLlFyC9kkq02aVZjaIIsubMN/NZ8s  tsunami.ocf.berkeley.edu (RSA)
    2048 MD5:55:0a:e3:4f:4b:2c:15:f8:d4:7d:f9:93:bf:a0:41:21 tsunami.ocf.berkeley.edu (RSA)

## SSH

Your shell account can be controlled remotely using
[SSH](https://en.wikipedia.org/wiki/Secure_Shell). The server name is
`ssh.ocf.berkeley.edu` (`tsunami`).

#### From your browser

If you just need to access SSH quickly, you can use our [web-based SSH
interface](https://ssh.ocf.berkeley.edu/) from your web browser.

#### Mac OS X, Linux, or Windows 10 (Version 1803 and above)

On Mac OS X, Linux, or Windows 10 (Version 1803 and above), enter in the terminal:

    ssh username@ssh.ocf.berkeley.edu

#### Windows

On Windows, use [PuTTY][putty] (download the `putty.exe` file):

* Host Name: `ssh.ocf.berkeley.edu`
* Port: 22

[putty]: https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html

#### Mosh

We also support [Mosh](https://mosh.org/), an SSH alternative with improved
support for laggy or roaming connections:

    mosh username@ssh.ocf.berkeley.edu

## SFTP

You can transfer files to your account using [SFTP][sftp]. To transfer files
you can use the command line utility `sftp`, or a graphical program such as
[FileZilla][filezilla] (Linux, Mac, Windows), [WinSCP][winscp] (Windows), or
[Cyberduck][cyberduck] (Mac, Windows).

[sftp]: https://en.wikipedia.org/wiki/SSH_File_Transfer_Protocol
[filezilla]: https://filezilla-project.org/
[winscp]: https://winscp.net/eng/index.php
[cyberduck]: https://cyberduck.io/

Otherwise, use the following information in your SFTP client.

* Protocol: SFTP (or SSH)
* Host Name: `ssh.ocf.berkeley.edu`
* Port: 22

## Disk quotas  {disk_quotas}

<!-- As amended by the Board of Directors on December 1, 2015. -->

Currently, accounts are limited to 15 GB of disk usage under the home and web
directories. You can check your disk usage by running `quota -v` over SSH or
[[from your browser|commands]].

## Unattended processes  {unattended_processes}

<!-- As established by the Board of Directors on April 17, 2017. SM can -->
<!-- unilaterally amend. -->

You are welcome to run unattended processes on the OCF. However, you are
ultimately responsible for ensuring that your unattended processes do not
unduly interfere with others’ ability to use the shared computing resources.

In particular, if you are going to run a batch job which may require a lot of
computing power, you are advised to run it under `nice` and/or `ionice` to
lower its CPU priority and I/O priority respectively. OCF staff reserve the
right to terminate or otherwise decrease the resource usage of processes which
are consuming too many resources.

If you’re trying to run a webapp or other kind of server process on the SSH
login server (`ssh.ocf.berkeley.edu`), please note that the SSH login server is
firewalled and what you’re trying to do unfortunately won’t work. If you’re a
group and you’re trying to run a webapp, you may want to consider
[[apphosting|doc services/webapps]] instead.
