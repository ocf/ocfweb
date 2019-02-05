[[!meta title="PHP"]]

`death`, the OCF webserver, currently runs PHP 7.0 with the following
non-standard packages installed:

* [APCu](http://php.net/manual/en/book.apcu.php) (opcode caching)
* [BC Math](http://php.net/manual/en/book.bc.php) (arbitrary precision math)
* [Bzip2](http://php.net/manual/en/book.bzip2.php) (compression library)
* [cURL](http://php.net/manual/en/book.curl.php) (networking library)
* [DBA](http://php.net/manual/en/book.dba.php) (database connector)
* [GD](http://php.net/manual/en/book.image.php) (graphics library)
* [MB String](http://php.net/manual/en/book.mbstring.php) (string encoding)
* [Mcrypt](http://php.net/manual/en/book.mcrypt.php) (cryptography library)
* [MySQL](http://php.net/manual/en/book.mysqli.php) (database connector)
* [SQLite](http://php.net/manual/en/book.sqlite.php) (database connector)
* [SOAP](http://php.net/manual/en/book.soap.php) (messaging protocol library)
* [XML](http://php.net/manual/en/book.xml.php) (markup parsing library)
* [ZIP](http://php.net/manual/en/book.zip.php) (compression library)

For a full list of available modules, run `phpinfo()` from a PHP script.
Plase [[contact us|doc contact]] if you are missing a module that you need
installed to get your application running.

## Custom PHP settings

If the default PHP settings are problematic for your site (for example, if you
require larger than normal file uploads), you can customize the PHP settings
used by creating [a `.user.ini` file][.user.ini] inside your web root.

In order to maintain compatibility with the OCF's PHP settings, we highly
recommend *not* copying an entire `php.ini`\* or `.user.ini` file from the web
or from another server. Instead, we advise you to create an empty `.user.ini`
and add only the settings you wish to change.

Note that `.user.ini` filename should be used, as our webserver will not look
for (per-user) `php.ini` files.

### Example `.user.ini` file

The following file, located at `~/public_html/.user.ini`, is an example of a
good `.user.ini` file.

    ; raise max upload and POST sizes
    upload_max_filesize = 32M
    post_max_size = 32M

    ; raise maximum number of input variables
    max_input_vars = 20000


[.user.ini]: https://secure.php.net/manual/en/configuration.file.per-user.php
