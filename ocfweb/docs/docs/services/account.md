[[!meta title="Account"]]


## Introduction

Your OCF account is both proof of your [[membership|doc membership]] and the
means by which you authenticate to the variety of [[services|doc services]]
operated by OCF [[staff|doc staff]]. Your OCF account is independent from
CalNet. (Technical info: public account information and salted password hashes
are stored in [[LDAP|doc staff/backend/ldap]] and [[Kerberos|doc
staff/backend/kerberos]] databases, respectively.)

Accounts are not normally deactivated after your membership [[eligibility|doc
membership/eligibility]] expires (e.g., graduation). In fact, we have active
accounts dating back to at least 1995.

## Passwords

OCF staff members **do not need to know your password**. In fact, we can't
"look it up" either since we don't store your password directly but rather a
salted [cryptographic
hash](https://en.wikipedia.org/wiki/Cryptographic_hash_function).

Email is generally insecure, so please **do not send passwords over email**. We
don't want to know it, and we have to disable your account if you tell it to
us!

### Changing your password

#### Using CalNet

You can [[find your username or reset your password online|change_password]]
using CalNet (assuming you have CalNet access).

To reset the password for a group account, you need to be a registered
signatory for the group. If your group isn't registered with the LEAD Center
(e.g. if it's a department-sponsored group), you will need to come in during
[[staff hours|staff-hours]] instead to reset the password.

#### Over SSH

You can change your password over SSH if you know your current password.

Use [[SSH|doc services/shell]] to run the command `passwd` and follow the
prompts as shown below. No text will appear when you are entering in a
password, just press enter when done after each prompt.

```text
$ passwd
myusername@OCF.BERKELEY.EDU's Password: <my current password>
New password: <my new password>
Verifying - New password: <my new password>
Success : Password changed
```

#### In person

If you are not able to use CalNet or SSH, or if you are a group and forgot your
current password, you can meet a staff member in person during [[staff
hours|staff-hours]].

Please bring sufficient documentation as listed on the [[membership
eligibility|doc membership/eligibility]] page to demonstrate that you are
authorized to reset the account password.

#### Manual verification of identity (typically for alumni with old accounts)    {manual-reset}

If you have forgotten your individual account password and are unable to use
CalNet or meet a staff member in person, you may reset your password through
our manual verification process.

You have two choices:

  * **Option 1 (email).** Send scanned copies of the documentation to a staff
    member over email. For security purposes, please **do not mail your
    documentation to any address listed on this website**. This gets archived
    and mailed out to all staff members.

    Instead, please email [help@ocf.berkeley.edu](mailto:help@ocf.berkeley.edu)
    and request to start the process (do **not** include any ID in the initial
    email). We'll provide a separate email for you to use instead to send in
    your documentation.

  * **Option 2 (postal mail).** Mail your documentation to our [[mailing
    address|doc contact#index6h2]]. Expect a delay of at least 2-3 weeks,
    possibly longer over summer.

For security purposes, please include the following with your request:

* a copy of your Cal ID

* a second piece of supporting ID (such as driver's license)

* a signed, dated statement to the effect of:
  > I, John Doe, authorize Open Computing Facility staff to reset my password.
  > Enclosed is a copy of my ID.

* contact information so that we can notify you when your password reset has
  been processed

If you no longer have your Cal ID, you may substitute it with another
government-issued ID.

Out of respect for your privacy, any copies of documents you send us will be
destroyed once we have verified your identity.

### MySQL

Access to your [[MySQL database|doc services/mysql]], if you have one, is
protected by a separate password.

## After graduation

Currently, we don't actively disable accounts, so you are free to use your
account until that policy changes. We can't promise all of your OCF account
privileges into perpetuity, however.  We are run by students volunteers using
student money.

## Disabled accounts

Some common reasons accounts are disabled:

 * by request
 * security (e.g., account hijacked)
 * misuse (e.g., excessive use of resources, violation of University policies)

Accounts may also be disabled if OCF staff need to contact you but cannot do
so.

To re-enable your account, you will need to see a Manager during [[staff
hours|staff-hours]].

If you want to disable your OCF account, please [[contact us|doc contact]] and
provide your OCF username. If your account appears to still be active, we may
ask for some evidence that you are the account owner. Currently, disabled
accounts are stored or archived and can be *re-enabled* by request at a later
date. Disabled accounts may eventually be scheduled for deletion.
