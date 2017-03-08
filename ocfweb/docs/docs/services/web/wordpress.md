[[!meta title="WordPress"]]

WordPress is a popular CMS (content management system) on the Web.

OCF's [[web hosting|doc services/web]] supports local WordPress installations,
and groups using WordPress are eligible for [[virtual hosting|doc
services/vhost]] (mygroup.berkeley.edu names).

Instructions for using WordPress are provided below; you can also [[drop by
during staff hours|staff-hours]] for in-person assistance.


## Installing WordPress

The easiest way to set up WordPress is via [[SSH|doc services/shell]]. Some
simple instructions:

1. Go to our [web-based SSH client](https://ssh.ocf.berkeley.edu/) and sign in
   with your username and password.

2. Create your web root by entering `makehttp` and hitting enter.

3. Create your MySQL database by entering `makemysql`. Copy the password it
   gives you -- you'll need it later.

4. Go to your web directory and download WordPress by entering these lines
   individually:

   ```shell
   cd ~/public_html
   wp core download
   ```

   This will download the latest version of WordPress into your web directory
   using [wp-cli](http://wp-cli.org/).

5. Visit your web admin dashboard and complete the installation process. Your
   website will be `https://www.ocf.berkeley.edu/~username` and the dashboard
   `https://www.ocf.berkeley.edu/~username/wp-admin`.

   You can choose whatever you want for most options, but you'll need to use:

   * **Database Name:** Your user name
   * **Database User Name:** Your user name
   * **Database Password:** Your MySQL password (the one you copied from step 3
     above)
   * **Database Host:** `mysql`
   * **Table Prefix:** Anything you want (the default `wp_` is fine)

Your WordPress installation is now ready! You can log in using the username and
password you created and start configuring your site.


## Migrating from WordPress.com to OCF

If you already have a site hosted at WordPress.com and you'd like to move it to
OCF web hosting, for example, to become eligible for [[virtual hosting|doc
services/vhost]], you can move most of your website's functionality and content
to the OCF's servers. Generally, the process is simple and sites migrated from
WordPress.com hosting to the OCF function quite well, apart from possible minor
differences in the appearance of themes. However, if you're looking to create
your website from scratch, in most cases it will be much easier to just install
WordPress on your OCF account and start editing it here, rather than creating
it locally or on another provider like WordPress.com and transferring things
over.

If you have an old WordPress installation lying around -- if you are replacing
an old student group website, for example -- you should archive it before
proceeding. See the example on our [[backup page|doc services/web/backups]] to
easily make a backup over SSH.

The basic steps to migration are as follows:

1. Follow the steps above to install WordPress on your OCF account.

2. Use the web admin dashboard to install all the themes and plugins you were
   using at WordPress.com

3. Log into your WordPress.com dashboard and go to `Settings > Export` to
   download a zipped XML file with all your site's posts and content. Note that
   this export usually will not include all of your media content.

4. Unzip this file and change the file extension of all .xml files to .wxr

5. Log into the dashboard at your OCF WordPress installation and go to `Tools >
   Import > WordPress`, then upload the .wxr file with all your content.

6. You will have to re-upload most of your media files to your OCF WordPress
   installation. Additionally, you should try and go through most of your posts
   and pages with images, as you may need to relink things again.

Further details can be found at [the support page by WordPress.com][1].

[1]: https://en.support.wordpress.com/moving-to-a-self-hosted-wordpress-site/


## Frequently Asked Questions

### Jetpack plugin not working

The Jetpack plugin as well as several others require a publicly accessible
XML-RPC file, which is not public by default. Before you can install Jetpack,
you need to add the following lines to the file `.htaccess` in your WordPress
folder:

```apache
<Files "xmlrpc.php">
  order allow, deny
  allow from all
</Files>
```

If `.htaccess` doesn't exist, create it and add the above lines.


### I forgot my admin password and can't log in

First, try using the "Forgot Password" feature on your site. You can find a
link from the login page.

If you're not able to recover your password via email, you can use
[wp-cli][wp-cli] instead, using the instructions below. (If you're not
comfortable following these instructions, consider coming in to [[staff
hours|staff-hours]] instead.


1. Go to our [web-based SSH client](https://ssh.ocf.berkeley.edu/) and sign in
   with your username and password.

2. Change directory to your WordPress installation (probably `~/public_html`,
   unless you changed it):

   ```shell
   cd ~/public_html
   ```

3. Figure out your username using the command `wp user list`. You should see
   output like the below:

   ```shell
   $ wp user list
   +----+------------+--------------+---------------+
   | ID | user_login | display_name | roles         |
   +----+------------+--------------+---------------+
   | 1  | admin      | Your Name    | administrator |
   +----+------------+--------------+---------------+
   ```

4. Reset your password using the username given above.

   ```
   $ wp user update admin --user_pass=new_password
   ```

   (Replace `admin` in the command above with your real username, and
   `new_password` with your new password.)


### I forgot my MySQL (database) password

The database password used by WordPress is recorded in the WordPress
configuration file `wp-config.php` on the line that looks like

```php
define('DB_PASSWORD', 'password_here');
```

If you ever need your password back, you can always find where WordPress is
installed (usually `~/public_html` or `~/public_html/wordpress`) and open
`wp-config.php` in an editor or get the password over SSH like so:

```shell
cat ~/path/to/wordpress/wp-config.php | grep DB_PASSWORD
```


### My site URL is configured incorrectly

If your site URL is configured incorrectly, you may have issues such as being
unable to log in or being caught in a redirect loop.

If that's the case, you can fix it by:

1. Go to our [web-based SSH client](https://ssh.ocf.berkeley.edu/) and sign in
   with your username and password.

2. Change directory to your WordPress installation (probably `~/public_html`,
   unless you changed it):

   ```shell
   cd ~/public_html
   ```

3. Run the following commands, substituting the correct URL for `example.com`:

   ```shell
   $ wp option update home 'https://example.com'
   $ wp option update siteurl 'https://example.com'
   ```


[wp-cli]: http://wp-cli.org/
