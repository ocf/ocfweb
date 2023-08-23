[[!meta title="Using Gmail with mail virtual hosting"]]

**Note:** Your berkeley.edu address is really just a branded Gmail account, so
these steps also work using your Berkeley email. You can use either a personal
or Berkeley email for these steps.

1. **Make sure you can receive mail.** This must be done before you can start
   sending mail.

   From the [[mail hosting configuration page|vhost_mail]], create a new
   mailing address for yourself. Make sure it forwards to your Gmail account:

   ![](https://i.fluffy.cc/zBz5DtjQbDpR7nGDrZXJnNDrtPDkxtmR.png)

   Once this is done, try sending yourself an email at your new address and
   make sure you receive it.

2. **Set a password for the email.** From the same page as before, make sure
   you've set a secure password for the email address.

   This is the password you'll use when configuring Gmail to send as your
   account.

3. **From Gmail, go to the settings page and start adding a new address.**

   From your Gmail account, click on the settings wheel in the top-right
   corner, then click "Settings".

   At the top of the Settings page, click the tab that says "Accounts".

   From this page, click "Add another email address you own".

4. **Fill out the name and email.**

   In the window that opened, fill out the first section with your name and the
   full email address. It's important to use the same email as in step 1.

   ![](https://i.fluffy.cc/pp80jlHtz7M7CVvN2qBTpjc8sVBXLx42.png)

   After filling this in, click "Next Step".

5. **Fill out the SMTP server details.**

   Use the following settings:

     * **SMTP Server:** `smtp.ocf.berkeley.edu`
     * **Username:** The *full email address*, including
       `@mygroup.studentorg.berkeley.edu` at the end.
     * **Password:** The password you chose in step 2.
     * **Port:** 587 (the default)
     * **Secured connection:** Using TLS (the default)

   It should look roughly like this:

   ![](https://i.fluffy.cc/Zk7LNFs9Brh2vn1vLnlCH2JbHqWQ6mln.png)

   Click "Add Account" when done.

6. **Verify the address.**

   You'll now be sent an email with a link to click to verify the address. This
   should have arrived at the same Gmail account.

   Click the link in that email and you're good to go!


From now on, when sending email via Gmail, you'll have a drop-down menu which
lets you select the "From" address, like this:

![](https://i.fluffy.cc/NlrKSbQG16MM6H2K6ZZF4l26D1pGBgjx.png)

If you use the Gmail app on your iPhone or Android device, you'll be able to
select the From address there as well.

**Having trouble with the above steps?** If you're stuck and can't figure out
what's wrong, feel free to [[drop by our staff hours|staff-hours]] for
in-person help!

As a last resort, you can also [[email us|doc contact]] for assistance. If you
do this, please provide as much detail as possible, including screenshots, the
email you're trying to use, and the steps you took. (But please *do not* send
us your password!)
