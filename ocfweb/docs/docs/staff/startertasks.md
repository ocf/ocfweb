[[!meta title="Starter Tasks"]]

Want to dive into learning about technical infrastructure at the OCF, but not
sure where to start? Here are some self-paced tasks you can do on your own. Feel
free to ask for help in our [Slack workspace](https://ocf.io/slack) or in person
during [staff hours](https://ocf.io/staffhours)!

Tasks marked with an asterisk (\*) require staff privileges. If you want to work
on these but aren't on staff, let a current staffer know you’re working on
 starter tasks and we will add you.

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

## Run the IRC bot in development mode\* (requires being on IRC)
Our chat bot is named `create` and its source code can be found at
https://github.com/ocf/ircbot. Before testing the IRC bot right away, make sure
you know how to use it:

1. Using your IRC client (or Slack), join the #test channel.
2. Trigger some bot commands. See https://ircbot.ocf.berkeley.edu/ for a list of
   commands. For example, saying `create: thanks` will trigger a response!
3. Find the source code for a particular command to learn how it works.

Once you’ve learned about `create`, you can start making changes to it!

1. Follow the steps in the GitHub README to run the bot in development mode.
2. Make sure you can talk to the bot in development mode-- it will be named
   `create-yourusername` instead of simply `create`.
3. Make a simple change and test that it works.
4. Bonus: figure out how to get your development bot to join a public channel
   like #test. (there are multiple ways to do this!)

## Play with staff utilities\*
OCF staff use a collection of scripts when interacting with the campus
community. For example, before creating an account for a student organization,
we make sure the person requesting the account is listed as a signatory for
that group. Staff members use the `signat` command to perform this check.

1. [Log into
   supernova](https://www.ocf.berkeley.edu/docs/staff/procedures/ssh-supernova/).
2. Use the `signat` command to list the signatories for the Open Computing
   Facility or another student organization of your choice.
3. Find the source code for this script on GitHub. Hint: if you’re not sure
which repository something is in, you can use [OCF
   Sourcegraph](https://sourcegraph.ocf.berkeley.edu) to search across all repositories!

## Play with your webspace
Every OCF account has [web
hosting](https://www.ocf.berkeley.edu/docs/services/web/) enabled at
https://www.ocf.berkeley.edu/~yourusername. As an example, check out
[ckuehl’s website](https://www.ocf.berkeley.edu/~ckuehl/).

1. Add some files to your webspace and preview it in your web browser.
2. (optional) Most student groups that host with the OCF use WordPress. Install
   WordPress in your webspace. (hint: instructions for this are on our website)

## Play with ocflib\*
[ocflib](https://github.com/ocf/ocflib) is a Python library we maintain which is
installed on every OCF host. For this exercise, you won’t need to make
modifications to ocflib.

1. Log into supernova and start an IPython3 shell (the `ipython3` command).
2. Run `import ocflib`.
3. Use ocflib functions to get the following information in your interactive
   Python shell:

    a. Get the list of signatories for the OCF, and your favorite student org.
    (hint: look at the signat source code from before!)

    b. Find the toner levels of each printer.
