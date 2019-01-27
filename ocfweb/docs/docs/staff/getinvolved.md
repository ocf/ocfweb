[[!meta title="Getting Involved"]]

## How can I get involved in the OCF?

Glad you asked! Students from all backgrounds are welcome to join staff. We
don’t interview or have a selective process for joining— you simply have to
express interest and show up to our weekly meetings. If you want to learn more
and be an active participant, there are multiple ways to get started:

### Stay up-to-date

We use a mailing list ([ocf.io/announce][announce]) to announce weekly meetings
and recap past meetings. If you’re joining in the middle of the semester or
missed a meeting, you can also read the mailing list archives to see what we
went over in the past. This is a low volume mailing list (2 emails per week)
and you can unsubscribe at any time.

[[Read more about other mailing lists available to join|doc
staff/mailing-lists]]

### In-person meetings

We hold two meetings every Monday:

#### Board of Directors (BoD)

**Mondays 7-8pm**

BoD is where we discuss and vote on administrative decisions. If you are
interested in gaining insight into the internal operations the OCF from an administrative
perspective, please come to BoD meetings! Meetings always are open to all.

#### Staff Meeting

**Mondays 8-9pm**

In these meetings, all OCF staff (that includes you!) get together to discuss
technology, learn from each other, and work on OCF projects. These meetings will
be a mix of presentations, work time, and socializing. Our goal is to build OCF
staff into a strong community of capable individuals.

### Contribute

We know that finding ways to contribute to the OCF can feel daunting, but we
don’t want you to be discouraged. Don’t worry about finding the best way to
contribute, as long as you find something that you want to work on. Here are
some ways to get started:

#### Projects

We have a curated list of projects at [ocf.io/projects][projects]. Projects
labeled “newbie” are ones we think are best fit for new staffers, but we are
happy to provide context and mentorship on any project. In general, don’t worry
about fully understanding the project description. If you find a something that
interests you, respond to the thread or reach out to a veteran staffer to get
more information.

#### GitHub Issues

All of our code is on GitHub ([github.com/ocf][ocf-github]). Sometimes you can find ways to
contribute by reading open issues, but they can sometimes be hard to understand
since they’re short on context. Some issues are also marked as “good first
issue.” Here’s a list of our most active repos, with some examples of things we
can do with them:

* [puppet][puppet] ([issues][puppet/issues]) - contains Puppet modules, which
  controls the software and configuration on all of our servers.
   * Install software packages on the desktops
     ([ocf_desktop/manifests/packages.pp][puppet-desktop-packages])
   * Configure Firefox to show the "are you sure you want to quit" dialog
     ([PR #373][puppet-373])
   * Allow operations staff to refund pages ([PR #368][puppet-368])
   * Monitor our mirrors to see if they’re out of date
     ([healthcheck script][mirror-healthcheck],
     [configuring server to call the healtcheck
     script][mirror-healthcheck-puppet],
     [Prometheus rules for alerting][prometheus-mirror])
   * Monitor printers to see if they’re out of paper, toner, or jammed
     ([printer.rules.yaml][prometheus-printer])
   * Send a desktop notification if a print jobs fails ([PR #321][puppet-321])
* [ocfweb][ocfweb] ([issues][ocfweb/issues]) - the source code for our website,
  www.ocf.berkeley.edu. Written in Python using the Django framework.
   * Hosts our documentation for users and staffers (including
     [this page][getinvolved-src]!) ([docs][docs-src])
   * JSON APIs for lab hours ([api/hours.py][api-hours])
   * [Account creation][account-register], [password resets][account-chpass],
     [others][account]
   * Lab usage statistics ([stats/][ocfweb-stats])
   * Form for requesting a virtual host ([account/vhost.py][ocfweb-vhost])
* [ocflib][ocflib] ([issues][ocflib/issues]) - a Python library installed on all
  servers. Has Python functions for various parts of the lab infrastructure.
   * Account management, searching ([account/][ocflib-account])
   * Accessing the database ([infra/mysql.py][ocflib-mysql])
   * Send automated emails ([misc/mail.py][ocflib-mail])
   * Printer querying and statistics ([printing/][ocflib-printing])
* [utils][utils] ([issues][utils/issues]) - similar to ocflib, this contains
  Python scripts that are run by humans.
   * Paper quota refund ([printing/paper][utils-paper])
   * Query/search OCF accounts ([acct/][utils-acct])
   * For users: create MySQL database and HTTP webdir
     ([makeservices/makemysql-real][utils-makemysql-real],
     [makeservices/makehttp][utils-makehttp])
   * Create new virtual machines ([staff/sys/makevm][utils-makevm])
   * Wake up desktops from sleep ([staff/lab/lab-wakeup][utils-lab-wakeup])
* [slackbridge][slackbridge] ([issues][slackbridge/issues]) - bridges our IRC
  network with our Slack organization, so staff members can exercise choice in
  what chat program they’d like to use. Written in Python.
* [ircbot][ircbot] ([issues][ircbot/issues]) - a fun chatbot, also used to
  approve new account requests. Written in Python.
   * See https://ircbot.ocf.berkeley.edu/ for a listing of IRC bot functionality

#### TODOs

If you’re feeling particularly adventurous, you can [search for the string
“TODO” across our entire codebase][sourcegraph-todo].

#### Help requests

During the semester, our [[help@ocf.berkeley.edu mailing list|doc contact]]
gets around 14 emails per week from the UC Berkeley community. These emails get
responded to by volunteers like you. Most requests are about requesting virtual
hosting and helping users debug or fix their websites. If you’re interested in
seeing how this process works, ask a staffer to add you to the RT mailing list.
Since this is high-volume, we recommend filtering these to a different folder
so you don’t get notified all the time.

Joining this list doesn’t obligate you to respond to help requests. It’s
perfectly acceptable to only read tickets as a way to learn more about what we
do.

If you’re on staff, you can view the ticket archive at [rt.ocf.berkeley.edu][rt].

#### Your idea here

As a volunteer organization, the OCF’s direction is driven by the interests of
our members. If you have a new idea for the OCF, we want to help you build it.
You can use our chat channels or talk to a veteran staffer in person to get a
starting point and roadmap.

### Staff Hours

During the week, veteran staffers host “staff hours”
([ocf.io/staffhours][staffhours]), where we provide support to users of our
services. As a newbie, attending staff hours can serve multiple purposes:

   * Learn by shadowing veteran staffers as they help people out
   * Talk about your interests so we can help you find stuff to work on
   * Get one-on-one mentoring so you can learn about the vast complex world of
     OCF infrastructure
   * Get context and more information on a particular area you’re interested
     in contributing in

### Slack or IRC

OCF staff often communicate on Slack or IRC. For instructions on how to join
Slack, see [ocf.io/slack][slack]. See [[IRC docs|doc contact/irc]] for how to
join IRC. Slack and IRC are bridged together, so joining either one lets you
participate in the same discussions. Some important channels:

   * #rebuild - technical discussion
   * #administrivia - non-technical discussion
   * #ocf for off-topic, non-OCF related discussion

These channels are typically very active, and you shouldn’t feel the need to
read every line to stay updated. You also aren’t required to understand all the
technical jargon that’s used in #rebuild. Feel free to introduce yourself in
any of these channels if you’re new, and don’t be afraid to ask questions!

### Hang out in the lab

OCF staff members usually like to socialize in the lab. We’re a friendly bunch,
so feel free to talk to us! You can also come into the lab after-hours— just
say you’re interested in joining staff and we’ll let you in.

## FAQ

**I wasn’t able to make the first/second/nth meeting of the semester, can I
still join?**

Yes! You can join at any time. If you’re worried about what you’ve missed, we
recommend reading archives from our mailing list ([ocf.io/announce][announce]).
These will usually contain links to presentations slides and information about
what was covered. You can also ask a veteran staffer to bring you up to speed.

**What if I can’t physically be present at weekly meetings?**

You can still be part of OCF staff as the suggestions on this page are useful
even if you can’t make meetings.

[account-chpass]: https://github.com/ocf/ocfweb/blob/master/ocfweb/account/chpass.py
[account-register]: https://github.com/ocf/ocfweb/blob/master/ocfweb/account/register.py
[account]: https://github.com/ocf/ocfweb/tree/master/ocfweb/account
[announce]: https://ocf.io/announce
[api-hours]: https://github.com/ocf/ocfweb/blob/master/ocfweb/api/hours.py
[docs-src]: https://github.com/ocf/ocfweb/tree/master/ocfweb/docs/docs
[getinvolved-src]: https://github.com/ocf/ocfweb/blob/master/ocfweb/docs/docs/staff/getinvolved.md
[ircbot/issues]: https://github.com/ocf/ircbot/issues
[ircbot]: https://github.com/ocf/ircbot
[mirror-healthcheck-puppet]: ️https://github.com/ocf/puppet/blob/master/modules/ocf_mirrors/manifests/monitoring.pp
[mirror-healthcheck]: https://github.com/ocf/puppet/blob/master/modules/ocf_mirrors/files/healthcheck
[ocf-github]: https://github.com/ocf
[ocflib-account]: https://github.com/ocf/ocflib/tree/master/ocflib/account
[ocflib-mail]: https://github.com/ocf/ocflib/blob/master/ocflib/misc/mail.py
[ocflib-mysql]: https://github.com/ocf/ocflib/blob/master/ocflib/infra/mysql.py
[ocflib-printing]: https://github.com/ocf/ocflib/tree/master/ocflib/printing
[ocflib/issues]: https://github.com/ocf/ocflib/issues
[ocflib]: https://github.com/ocf/ocflib
[ocfweb-vhost]: https://github.com/ocf/ocfweb/blob/master/ocfweb/account/vhost.py
[ocfweb-stats]: https://github.com/ocf/ocfweb/tree/master/ocfweb/stats
[ocfweb/issues]: https://github.com/ocf/ocfweb/issues
[ocfweb]: https://github.com/ocf/ocfweb
[projects]: https://ocf.io/projects
[prometheus-mirror]: https://github.com/ocf/puppet/blob/master/modules/ocf_prometheus/files/rules.d/mirror.rules.yaml
[prometheus-printer]: https://github.com/ocf/puppet/blob/master/modules/ocf_prometheus/files/rules.d/printer.rules.yaml
[puppet-321]: https://github.com/ocf/puppet/pull/321
[puppet-368]: https://github.com/ocf/puppet/pull/368
[puppet-373]: https://github.com/ocf/puppet/pull/373
[puppet-desktop-packages]: https://github.com/ocf/puppet/blob/master/modules/ocf_desktop/manifests/packages.pp
[puppet/issues]: https://github.com/ocf/puppet/issues
[puppet]: https://github.com/ocf/puppet
[rt]: https://rt.ocf.berkeley.edu/
[slack]: https://ocf.io/slack
[slackbridge/issues]: https://github.com/ocf/slackbridge/issues
[slackbridge]: https://github.com/ocf/slackbridge
[sourcegraph-todo]: https://sourcegraph.ocf.berkeley.edu/search?q=TODO
[staffhours]: https://ocf.io/staffhours
[utils-acct]: https://github.com/ocf/utils/tree/master/acct
[utils-lab-wakeup]: https://github.com/ocf/utils/blob/master/staff/lab/lab-wakeup
[utils-makehttp]: https://github.com/ocf/utils/blob/master/makeservices/makehttp
[utils-makemysql-real]: https://github.com/ocf/utils/blob/master/makeservices/makemysql-real
[utils-makevm]: https://github.com/ocf/utils/blob/master/staff/sys/makevm
[utils-paper]: https://github.com/ocf/utils/blob/master/printing/paper
[utils/issues]: https://github.com/ocf/utils/issues
[utils]: https://github.com/ocf/utils
