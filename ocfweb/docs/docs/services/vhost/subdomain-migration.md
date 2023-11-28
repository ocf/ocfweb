[[!meta title="Subdomain migration FAQ"]]

All student organizations that currently have berkeley.edu subdomains (e.g. myclub.berkeley.edu) will have them transitioned to be under studentorg.berkeley.edu (e.g. myclub.studentorg.berkeley.edu) by the end of the 2023-24 academic year. There are different timelines and instructions depending on the type of website that you have, so please review the details for the option that best matches your group. We have additional instructions at the bottom for groups that have email addresses at their domain as well.

## WordPress sites
* Your club's website is now also accessible at myclub.studentorg.berkeley.edu in addition to your current myclub.berkeley.edu domain
* On March 1, 2024, we will be forcing a redirect from myclub.berkeley.edu to myclub.studentorg.berkeley.edu
  * This means that users trying to access any page on myclub.berkeley.edu will be redirected to that respective page at myclub.studentorg.berkeley.edu
* We will be automating the transition for WordPress sites, but we will ask that you review your site on March 1, 2024 and make sure that everything works correctly
* If you have forgotten your group's OCF username or password, any signatory can visit https://ocf.io/password and view the username or reset the password
* You can access your site's WordPress admin dashboard at https://myclub.berkeley.edu/wp-admin
  * After March 1, 2024 you will be able to access your site's WordPress admin dashboard at https://myclub.studentorg.berkeley.edu/wp-admin instead
  * If you have forgotten your group's WordPress admin credentials, we have instructions on how to reset your password at https://ocf.io/wordpress#h3_i-forgot-my-admin-password-and-cant-log-in

## All other virtual hosting sites
* Your club's website is now also accessible at myclub.studentorg.berkeley.edu in addition to your current myclub.berkeley.edu domain
* On April 1, 2024, we will be forcing a redirect from myclub.berkeley.edu to myclub.studentorg.berkeley.edu
  * This means that users trying to access any page on myclub.berkeley.edu will be redirected to that respective page at myclub.studentorg.berkeley.edu
* If you have hardcoded your domain anywhere in your website's source code or in your database, please update that before the transition period ends or your users may end up in a redirect loop and will be unable to access your site
* If you have forgotten your group's OCF username or password, any signatory can visit https://ocf.io/password and view the username or reset the password
* You can access your website's files over SSH or SFTP, we have documentation on how to do this at https://ocf.io/ssh
* If your group would like to transition from myclub.berkeley.edu to myclub.studentorg.berkeley.edu early before the April 1, 2024 deadline, please fill out this form and OCF will update your domain within 48 hours: https://forms.gle/xxy3NrKC6wd28ibm9

## App hosting sites
* Your club's website is now also accessible at myclub.studentorg.berkeley.edu in addition to your current myclub.berkeley.edu domain
* On April 1, 2024, we will be forcing a redirect from myclub.berkeley.edu to myclub.studentorg.berkeley.edu
  * This means that users trying to access any page on myclub.berkeley.edu will be redirected to that respective page at myclub.studentorg.berkeley.edu
* If you have hardcoded your domain anywhere in your website's source code or in your database, please update that before the transition period ends or your users may end up in a redirect loop and will be unable to access your site
* If you have forgotten your group's OCF username or password, any signatory can visit https://ocf.io/password and view the username or reset the password
* You can access your website's files over SSH or SFTP, we have documentation on how to do this at https://ocf.io/ssh
  * You will need to SSH into `apphost.ocf.berkeley.edu` instead of `ssh.ocf.berkeley.edu` as described in the article (your credentials will be the same though)
  * If you need a refresher on how OCF app hosting works, we have documentation at https://ocf.io/apphost
* If your group would like to transition from myclub.berkeley.edu to myclub.studentorg.berkeley.edu early before the April 1, 2024 deadline, please fill out this form and OCF will update your domain within 48 hours: https://forms.gle/xxy3NrKC6wd28ibm9

## Mail virtual hosting
* We have already updated your email addresses to use myclub.studentorg.berkeley.edu
  * Any emails sent to myclub.berkeley.edu will be redirected to the respective address at myclub.studentorg.berkeley.edu
  * You can review these addresses at https://www.ocf.berkeley.edu/account/vhost/mail/
* Everyone who sends emails from a myclub.berkeley.edu email address will need to change their sender address to send from myclub.studentorg.berkeley.edu
  * We have documentation on how to do this at https://www.ocf.berkeley.edu/docs/services/vhost/mail/gmail/
  * For example, if your old email address was president@myclub.berkeley.edu, you will need to:
    1. Add president@myclub.studentorg.berkeley.edu to Gmail following the instructions above
    2. Delete president@myclub.berkeley.edu from Gmail at https://mail.google.com/mail/u/0/#settings/accounts
