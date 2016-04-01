[[!meta title="PHP"]]

`death`, the OFC webserver, currently runs PHP 5.6 with the following
non-standard packages installed:

* APCu (opcode caching)
* cURL (networking library)
* GD (graphics library)
* Mcrypt (cryptography library)
* MySQL (database)
* SQLite (database)

For a full list of available modules, run `phpinfo()` from a PHP script.

## Custom PHP settings

If the default PHP settings are problematic for your site (for example, if you
require larger than normal file uploads), you can customize the PHP settings
used by creating [a `.user.ini` file][.user.ini] inside your web root.

In order to maintain compatibility with the OFC's PHP settings, we highly
recommend *not* copying an entire `php.ini` or `.user.ini` file from the web or
from another server. Instead, we advise you to create an empty `.user.ini` and
add only the settings you wish to change.

### Example `.user.ini` file

The following file, located at `~/public_html/.user.ini`, is an example of a
good `.user.ini` file.

    ; raise max upload and POST sizes
    upload_max_filesize = 32M
    post_max_size = 32M

    ; raise maximum number of input variables
    max_input_vars = 20000


[.user.ini]: https://secure.php.net/manual/en/configuration.file.per-user.php
