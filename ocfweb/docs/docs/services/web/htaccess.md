[[!meta title="Password protecting pages (htaccess)"]]


A simple way to add password protection to parts of your website or the whole of your website is by using a `.htaccess` file, paired with a `.htpasswd` file. These dotfiles (named such since they begin with a dot, and are regularly hidden unless you list them with `ls -a`) are able to restrict access to files based on the settings you input. 

To password protect an entire website:

To password protect a subset of files:

TO password protect a single file:

In order to access the files, you must enter a log-in. This will appear as a window alert asking for a username and password. For the sake of demonstration, we will use "admin" and "password", however, you are strongly recommend to use a secure password.

Log-ins are configured in your `.htpasswd` files. Create one by using the command `htpasswd -c " 


