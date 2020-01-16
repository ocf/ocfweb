[[!meta title="Starter Tasks"]]

Want to dive into learning about technical infrastructure at the OCF, but not
sure where to start? Here are some self-paced tasks you can do on your own. Feel
free to ask for help in our [Slack workspace](https://ocf.io/slack) or in person
during [staff hours](https://ocf.io/staffhours)!

Tasks marked with an asterisk (\*) require staff privileges. If you want to work
on these but haven't officially been given staff privileges yet, let a current
staffer know you’re working on starter tasks and we will add you.

These tasks don’t have to be completed in order.

## Connect to the OCF IRC network
Internet Relay Chat (IRC) is a chat protocol invented in the 80s, an early
precursor to Slack. The OCF runs an IRC server (since 2002!), which is bridged
to our Slack network. Many staffers prefer IRC to Slack due to its wide breadth
of customizable clients, as opposed to Slack, which requires using their
application.

For this task, pick an IRC client, install it on your computer, and use it to
connect to the OCF IRC network (details at https://ocf.io/irc). Some popular
clients are:

* Irssi (Mac/Linux, console)
* Weechat (Max/Linux, console)
* Hexchat (Windows/Linux, graphical)
* Colloquy (Mac, graphical)

See http://www.irchelp.org/clients/ for more recommendations.

Once you’ve joined IRC, pick any channel (#rebuild, #henlo, etc) and say hi!

## Get familiar with the command line
All of [[our servers|doc staff/backend/servers]] run Linux, and we interact with
them over the command line. There are a lot of online resources about using the
Linux command line, so if you're confused about something, try Googling it!

If you haven't used the command line before, you can go to our [[command
reference|doc services/shell/commands]] page and try running some commands. You
can also connect to [[our ssh server|doc services/shell]]
(`ssh.ocf.berkeley.edu`) using your own SSH client.

If you want to get more comfortable, try completing [lab
1](https://decal.ocf.berkeley.edu/labs/b1) from the OCF/XCF Linux System
Administration DeCal.

## Run the IRC bot in development mode\* (requires being on IRC)
Our chat bot is named `create` and its source code can be found at
https://github.com/ocf/ircbot. Before testing the IRC bot right away, make sure
you know how to use it:

1. Using your IRC client (or Slack), join the #test channel.
2. Trigger some bot commands. See https://ircbot.ocf.berkeley.edu/ for a list of
   commands. For example, saying `create: thanks` will trigger a response!
3. Find the source code for a particular command to learn how it works.

Once you’ve learned about `create`, you can start making changes to it!

1. Follow the steps in the [GitHub README](https://github.com/ocf/ircbot) to run
   the bot in development mode.
2. Make sure you can talk to the bot in development mode-- it will be named
   `create-yourusername` instead of simply `create`.
3. Make a simple change and test that it works.
4. Bonus: figure out how to get your development bot to join a public channel
   like #test. (there are multiple ways to do this!)

## Play with staff utilities\*
OCF staff use a collection of scripts when interacting with the campus
community. For example, before creating an account for a student organization,
we make sure the person requesting the account is listed as a signatory for that
group. Staff members use the
[`signat`](https://ocf.io/docs/staff/scripts/signat) command to perform this
check.

1. [[Log into supernova|doc staff/procedures/ssh-supernova]].
2. Use the `signat` command to list the signatories for the Open Computing
   Facility or another student organization of your choice. Hint: if you are not
   sure how to use the `signat` command, try running `signat --help`. This trick
   works with most commands. OCF scripts also have [[documentation on this
   website|doc staff/scripts/signat]].
3. Find the source code for this script on GitHub. Hint: if you’re not sure
   which repository something is in, you can use [OCF Sourcegraph][sourcegraph]
   to search across all repositories!

## Play with your webspace
Every OCF account has [[web hosting|doc services/web]] enabled at
https://www.ocf.berkeley.edu/~yourusername. As an example, check out [ckuehl’s
website](https://www.ocf.berkeley.edu/~ckuehl/).

1. Add some files to your webspace and preview it in your web browser.
2. (optional) Most student groups that host with the OCF use WordPress. Install
   WordPress in your webspace. (hint: instructions for this are on our website)

## Play with ocflib\*
[ocflib][ocflib] is a Python library we maintain which is installed on every OCF
host. For this exercise, you won’t need to make modifications to ocflib.

1. [[Log into supernova|doc staff/procedures/ssh-supernova]] and start an
   IPython3 shell (the `ipython3` command).
2. To make sure things are working:
   1. Run `import ocflib.lab.staff_hours` to import utilities relating to
      [[staff hours|staff-hours]].
   2. Run `staffhours = ocflib.lab.staff_hours.get_staff_hours()` to get the
      list of staff hours.
   3. Take a look at the list `staffhours` and check that it matches the info
      on [[the staff hours page|staff-hours]]. For instance, you should be able
      to run `staffhours[0]` to see the info corresponding to the first staff
      hour entry on the page.
3. Your turn! Use ocflib functions to get the following information in your
   interactive Python shell:
   1. Get the list of signatories for the OCF, and your favorite student org.
   (hint: look at the signat source code from before!)
   2. Find the toner levels of each printer.
   3. Find the hours the OCF was open on your most recent birthday.

   If you get stuck, don't forget that you can search the [GitHub repo][ocflib]
   or [Sourcegraph][sourcegraph] to find more info.

[ocflib]: https://github.com/ocf/ocflib
[sourcegraph]: https://sourcegraph.ocf.berkeley.edu
