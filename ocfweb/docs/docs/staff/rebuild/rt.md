[[!meta title="Request Tracker"]]

**Note:** RT is now deployed as a Marathon service running in Docker, so these
instructions aren't super useful for OCF staff. This page is kept as a
reference for others who might come across it (it ranks pretty highly on
Google). If you're one of these people, you might find one of these useful:

  * [Our Puppet code for installing RT.][rt-puppet]
    We don't actually use this anymore, but it should be reasonably modern and
    worked well for us for a long time.

  * [Our Dockerized RT service.][rt-docker]
    We run this on Marathon, but you should easily be able to get it running on
    something like Kubernetes or Docker Swarm, too.

## Installation

Both Apache 2 and Nginx installation are listed below. Pick your poison...

1. Install required packages:

       sudo aptitude install mysql-server
       sudo aptitude install -t squeeze-backports request-tracker4 rt4-db-mysql

   **For Apache 2:** Install

       sudo install libapache-mod-auth-kerb
       sudo install -t squeeze-backports rt4-apache

   **For Nginx:** Install

       sudo install -t squeeze-backports nginx rt4-fcgi

   and enable the RT FastCGI daemon: in `/etc/default/rt4-fcgi`, edit:

       enabled=1

   Debian packages an obscenely old version of Nginx in stable, so please don't
   install that. People will laugh at you.

   Configuration by debconf:
   - Name: rt.ocf.berkeley.edu
   - Handle RT_SiteConfig.pm permissions: yes
   - SQL password: ....

   Install RT::Extension::CommandByMail and RT::Extension::MergeUsers:

       sudo cpan
       cpan> install RT::Extension::CommandByMail
       cpan> notest install RT::Extension::MergeUsers

   When prompted, the RT lib folder is located at
   `/usr/share/request-tracker4/lib`.

1. Copy site-specific RT configuration into
   `/etc/request-tracker4/RT_SiteConfig.d/99-ocf`: (this should be puppeted)

   ```perl
   # Debug - commented out for now
   #Set($LogToSTDERR, "debug");
   #Set($LogToSyslog, "debug");

   Set($WebDomain, 'rt.ocf.berkeley.edu');
   Set($WebBaseURL , "https://rt.ocf.berkeley.edu");
   Set($WebPort, 443);

   # Use external authentication provided by mod_auth_kerb
   Set($WebExternalAuth , 1);
   Set($WebFallbackToInternalAuth, 1);
   # tells RT to create users automatically if no user matching REMOTE_USER is found
   Set($WebExternalAuto, 1);
   Set($WebExternalGecos, undef);

   # Plugins
   Set(@MailPlugins, qw(Auth::MailFrom Filter::TakeAction));
   Set(@Plugins,(qw(RT::Extension::CommandByMail RT::Extension::MergeUsers)));

   # Make links clicky
   Set(@Active_MakeClicky, qw(httpurl_overwrite));

   # Non-fail To addresses
   Set($UseFriendlyToLine, 1);

   # Enable fulltext
   Set( %FullTextSearch,
       Enable     => 1,
       Indexed    => 1,
       Table      => 'AttachmentsIndex',
       MaxMatches => '10000',
   );

   # Use plain text instead of HTML email
   Set($MessageBoxRichText, undef);
   Set($PreferRichText, undef);
   ```

   Regenerate the resultant `RT_SiteConfig.pm` file:

       sudo update-rt-siteconfig

6. Ensure that SSL certificates for `rt.ocf.berkeley.edu` exist at the
   following locations:
   * Certificate: `/etc/ssl/private/rt_ocf_berkeley_edu.crt`
   * Certificate chain/bundle: `/etc/ssl/private/incommon.crt`
   * Private key: `/etc/ssl/private/rt_ocf_berkeley_edu.key`

   **Nginx only:** Create a "chained" certificate file:

       cat rt_ocf_berkeley_edu.crt incommon.crt > rt_ocf_berkeley_edu.chained.crt

7. **For Apache 2:** Copy the following RT configuration file `rt` into
   `/etc/apache2/sites-available` and link to it from
   `/etc/apache2/sites-enabled` (replace typhoon.ocf.berkeley.edu with the FQDN
   reported by `hostname -f`):

   ```apache
   # Apache configuration file for RT

   <VirtualHost *:80>
           ServerName rt.ocf.berkeley.edu
           RewriteEngine On
           RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
   </VirtualHost>

   <VirtualHost *:443>
           ServerName rt.ocf.berkeley.edu

           SSLEngine on
           SSLCertificateFile /etc/ssl/private/rt_ocf_berkeley_edu.crt
           SSLCertificateChainFile /etc/ssl/private/incommon.crt
           SSLCertificateKeyFile /etc/ssl/private/rt_ocf_berkeley_edu.key

           Alias /rt /usr/share/request-tracker4/html
           RedirectMatch ^/$ /rt

           <Location /rt>
                   SetHandler modperl
                   PerlResponseHandler Plack::Handler::Apache2
                   PerlSetVar psgi_app /usr/share/request-tracker4/libexec/rt-server

                   # Comment this to enable RT-local root
                   AuthType Kerberos
                   Require valid-user
                   KrbMethodNegotiate On
                   KrbMethodK5Passwd On
                   KrbLocalUserMapping On
                   KrbServiceName HTTP/typhoon.ocf.berkeley.edu
                   Krb5KeyTab /etc/apache2/sites-available/rt.keytab
           </Location>

           <Location /rt/REST/1.0/NoAuth>
                   # No Kerberos - for rt-mailgate
                   Satisfy Any
                   Order Allow,Deny
                   Allow from 128.32.129.218 # sandstorm.ocf.berkeley.edu
           </Location>

           <Location /rt/NoAuth>
                   # No Kerberos - login/logout pages
                   Satisfy Any
                   Order Allow,Deny
                   Allow from All
           </Location>

           <Perl>
                   use Plack::Handler::Apache2;
                   Plack::Handler::Apache2->preload("/usr/share/request-tracker4/libexec/rt-server");
           </Perl>

   </VirtualHost>
   ```

   **For Nginx:** Copy the following RT configuration file `rt` into
   `/etc/nginx/sites-available` and link to it from `/etc/nginx/sites-enabled`:

   ```nginx
   # Configuration for RT on Nginx
   # rt.ocf.berkeley.edu

   server {
           listen 80;
           server_name rt.ocf.berkeley.edu;
           rewrite ^ https://$server_name$request_uri? permanent;
   }

   server {
           listen 443;
           server_name rt.ocf.berkeley.edu;
           rewrite ^/$ /rt;

           root /usr/share/request-tracker4;

           location /rt {
                   # See /usr/share/doc/rt4-fcgi/examples/request-tracker4.conf
                   expires epoch;

                   # Require the default authentication on typhoon (pam_krb5)
                   auth_pam "RT";
                   auth_pam_service_name "common-password";

                   # Proxy over to rt4.
                   fastcgi_pass unix:/var/run/rt4-fcgi.sock;
                   include /etc/nginx/fastcgi_params;
                   fastcgi_param REMOTE_USER $remote_user;
                   fastcgi_param SCRIPT_NAME "/rt";
           }

           # Bypass FastCGI for images
           location /rt/NoAuth/images {
                   alias           /usr/share/request-tracker4/html/NoAuth/images/;
           }

           location /rt/REST/1.0/NoAuth {
                   allow           128.32.129.218; # sandstorm.ocf.berkeley.edu
                   deny            all;

                   fastcgi_pass unix:/var/run/rt4-fcgi.sock;
                   include /etc/nginx/fastcgi_params;
                   fastcgi_param REMOTE_USER $remote_user;
                   fastcgi_param SCRIPT_NAME "/rt";
           }

           ssl on;

           # Same as apache
           ssl_certificate /etc/ssl/private/rt_ocf_berkeley_edu.chained.crt;
           ssl_certificate_key /etc/ssl/private/rt_ocf_berkeley_edu.key;

           ssl_session_timeout 5m;
           ssl_session_cache shared:SSL:10m;

           ssl_protocols SSLv3 TLSv1;
           ssl_ciphers ALL:!ADH:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv3:+EXP;
           ssl_prefer_server_ciphers on;
   }
   ```

8. **Apache 2 only:** Obtain a keytab for the principal
   HTTP/typhoon.ocf.berkeley.edu@OCF.BERKELEY.EDU (replace
   typhoon.ocf.berkeley.edu with the FQDN reported by `hostname -f`) and place
   it into `/etc/apache2/sites-available/rt.keytab`. Make sure it's only
   readable by www-data.

8. mod_auth_kerb/ngx_http_auth_pam uses HTTP Basic authorization which has no
   concept of login/logout. Emulate logout behavior by changing the Logout page
   to send a 401 (works for Chrome), run proprietary IE code (works for IE),
   and make an Ajax call to a non-existing page with bad credentials (works for
   Firefox).

   The below code has been "adapted" from https://trac-hacks.org/wiki/TrueHttpLogoutPatch

   This should be fixed so that RT's installation files aren't being directly modified.

   Edit `/usr/share/request-tracker4/html/NoAuth/Logout.html`:

   Change

       <& /Elements/Header, Title => loc('Logout'), Refresh => RT->Config->Get('LogoutRefresh') &>

   to

       <& /Elements/Header, Title => loc('Logout') &>

   and paste the following below it:

       <script type="text/javascript">
       function clearAuthenticationCache() {
         try {
           var agent = navigator.userAgent.toLowerCase();
           if (agent.indexOf("msie") != -1) {
             // This works only on IE only.
             document.execCommand("ClearAuthenticationCache");
           }
           else {
             var xml = createXMLObject();
             // Let's prepare invalid credentials
             xml.open("GET", Math.random().toString(), true, "logout", "logout");
             xml.send("");
             xml.abort();
           }
         } catch (e) {
           return;
         }
       }

       function createXMLObject() {
         try {
           if (window.XMLHttpRequest) {
             xml = new XMLHttpRequest();
           }
           else if (window.ActiveXObject) {
             xml = new ActiveXObject("Microsoft.XMLHTTP");
           }
         } catch (e) {
           xml = false
         }
         return xml;
       }

       clearAuthenticationCache();
       </script>

   Add the following before the end of the <%INIT> block at the end of the file:

       # "Force" logout due to using mod_auth_kerb -- Chrome
       $HTML::Mason::Commands::r->status(401);

   Clear the RT Mason cache.

       sudo rm -rf /var/cache/request-tracker4/*

8. **For Apache 2:** Restart Apache.

   **For Nginx:** Restart the RT FastCGI daemon.

       sudo service rt4-fcgi restart

9. Install the RT [mailgate
   program](http://requesttracker.wikia.com/wiki/EmailInterface#RT.27s_mail_gate)
   on the mail server.

   squeeze-backports is required here too.

       sudo aptitude install rt4-clients

10. Set up rt@ocf.berkeley.edu to feed mail into rt-mailgate.

    Add or edit the following lines into `/var/mail/aliases/aliases`:

        rt: "|/usr/bin/rt-mailgate --queue General --action correspond --url https://rt.ocf.berkeley.edu/rt"
        rt-comment: "|/usr/bin/rt-mailgate --queue General --action comment --url https://rt.ocf.berkeley.edu/rt"

## Configuration

1. The RT root user can't log in while Kerberos password authentication is
   enabled because of the way `mod_auth_kerb/ngx_http_auth_pam` works. So, you
   must first log in with Kerberos credentials to create a user from Kerberos
   and grant superuser rights on it.

   Log in to RT. You will be auto-created and redirected to Self-Service.
   Disable Kerberos password authentication:

   **Apache 2:** Comment out the following lines in `/etc/apache2/sites-available/rt`:

       # AuthType Kerberos
       # Require valid-user

   and force-reload Apache configuration (`service apache2 force-reload`).

   **Nginx:** Comment out the following lines in `/etc/nginx/sites-available/rt`:

       # auth_pam "RT";
       # auth_pam_service_name "common-password";

   and restart Nginx (`service nginx restart`).

1. Visit RT again and log in as RT root.

   Go to Tools > Configuration > Users > Select, and type in your username in
   "Go to user". Enable **Let this user be granted rights (Privileged)**.

   Go to Tools > Configuration > Global > User Rights. On the left side, in Add
   User, type your name. Then, on the right side, click the tab **Rights for
   Administrators**, and enable **Do anything and everything**.

   Save changes.

   You will want to remove your superuser powers later because superusers may
   be artificially limited in rights elsewhere on RT for your own protection:
   ["Starting from version 3.2 (or 3.4?) RT doesn't show users with the
   SuperUser right in a ticket owner
   select-box."](http://requesttracker.wikia.com/wiki/SuperUser)

   Re-enable Kerberos password authentication in Apache configuration and
   force-reload Apache.

1. Create groups. I've created root and staff groups; this configuration may
   change as our use of RT is refined.

   Go to Tools > Configuration > Groups > Create and create "Root" and "Staff"
   groups.

   Add users to these groups by the **Members** subsection in the upper right
   corner of the group modification page. (You can also alter a user's group
   memberships from the user's modification page.)

   In this configuration I see the set of RT privileged users to be the same as
   the set of users in group "Staff". This may change.

2. Enable user rights. [This](http://requesttracker.wikia.com/wiki/Rights)
   guide is being followed.

   Go to Tools > Configuration > Global > Group Rights.

   **Save your changes each time you make changes to a group's rights.**

   Make sure the selected group is **Everyone**.

   Select the following rights:
   - Comment on tickets
   - Create tickets
   - Reply to tickets
   - View queue
   - View ticket summaries

   Now add a group to add permissions to, from the bottom left: Add Group

   Add these rights to "Staff", in the "Rights for Staff" tab:
   - Delete tickets
   - Modify one's own RT account
   - Modify tickets
   - Own tickets
   - Steal tickets
   - Take tickets
   - View private ticket commentary

   Add these rights to "Root", in the "Rights for Administrators" tab:
   - Everything except "Do anything and everything"

3. Miscellaneous configuration

   Change RT root's info so he can be a front for staff@. (Tools >
   Configuration > Users > Select, click root, change email to
   staff@ocf.berkeley.edu and Real Name to OCF Staff).

   Make the General queue sound better: Tools > Configuration > Queues >
   Select, click General, change Description to "OCF Staff". (I think changing
   the Queue Name would be nice too. If you do that, remember to change the
   parameters to rt-mailgate in `/var/mail/aliases/aliases` and re-run
   newaliases on sandstorm.)

   Add root as a watcher for General so staff@ gets automatically Cc'ed to new
   tickets. Click Watchers in the upper right corner and add root.

4. Send more mail.

   By default RT only sends an autoreply to the requestor on ticket creation.
   Create a new scrip (RT callback) so that Cc (staff@) gets notified on ticket
   creation as well.

   Create that which is to be mailed: go to Tools > Configuration > Global >
   Templates > Create.

   Create a template with the name "Correspondence Creation" and description
   "For mailing staff on ticket creation, but without all that boilerplate".
   Keep type as "Perl". Paste this in as the content:

       RT-Attach-Message: yes
       Subject: {$Ticket->Subject}

       {$Transaction->Content()}

   Save changes.

   Modify the scrip "On Create Notify AdminCcs" to use the template "Global Template: Correspondence Creation".

4. Send spoofed mail.

   Mail in the past has come from actual people, not endless drones of "via
   RT". Let's fake that for people who are uncomfortable with change. At the
   top of Correspondence, Admin Correspondence, Admin Comment, and
   Correspondence Creation templates, append the following below the last mail
   header that appears, if any exist:

       From: {
         my $u = $Transaction->CreatorObj;
         my $a = $u->EmailAddress;
         my $res = $u->RealName || $u->Name;
         $res .= " <".$a .">" ;
       $res; }

5. Automatically close tickets.

   This needs to be chained or something to send a template saying that the
   ticket is closed because it hasn't been modified in 30 days. I don't know
   what this entails, but the below is a start.

   Put the following into a crontab; you may want to create a rt system user to
   run this.

       0 * * * * /usr/bin/rt-crontool --search RT::Search::FromSQL \
       --search-arg "LastUpdated < '5 days ago' AND Status = 'stalled'" \
       --action RT::Action::SetStatus --action-arg resolved

   References:
   [1](http://lists.bestpractical.com/pipermail/rt-users/2005-February/028837.html)
   [2](http://requesttracker.wikia.com/wiki/UntouchedInHours)
   [3](http://requesttracker.wikia.com/wiki/TimedNotifications)

## Notes

* First-time autocreated users will have incorrect/embarrassing Real Names (for
  some reason, it grabs the gecos on occasion), so that should be fixed upon
  first login. Users can also update this information when they feel like it.

## Todo

* Fix Chrome double login, if possible.
  * Doesn't occur when running Nginx, only Apache 2.
* Set up ticket autoclose using
  http://requesttracker.wikia.com/wiki/UntouchedInHours or
  http://requesttracker.wikia.com/wiki/TimedNotifications

## References

* http://requesttracker.wikia.com/wiki/HomePage

[rt-puppet]: https://github.com/ocf/puppet/tree/fc6d4242ba773cefbc9e7c1ea542f8f7de3e8785/modules/ocf_rt
[rt-docker]: https://github.com/ocf/rt
