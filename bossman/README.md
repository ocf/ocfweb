bossman is a lightweight API which accepts requests for account-related changes
and performs them synchronously.

For security reasons, bossman is run on a separate server from the main atool
web service.

This is *not* a public API. In its current state, all requests received are
considered to be trusted; the web server is responsible for doing some kind of
authentication (probably HTTP client certs in the short term, and GSSAPI/SPNEGO
eventually).

Valid requests:

## POST /account (create account)
### Request body example:

Content-Type: `application/json`

    {
        "uid": "ckuehl",
        "cn": "Chris Kuehl",
        "password": "hunter2",
        "mail": "ckuehl@berkeley.edu",
        "calnetUid": "1034192"
    }

### Response codes

* 201 Created
* 400 Bad Request
  * Response body will contain an error in arbitrary format.
* 500 Internal Server Error
  * Response body may contain an error in arbitrary format.
