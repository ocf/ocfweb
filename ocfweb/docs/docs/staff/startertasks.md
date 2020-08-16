[[!meta title="Starter Tasks"]]

Want to dive into learning about technical infrastructure at the OCF, but not
sure where to start? Here are some self-paced tasks you can do on your own. Feel
free to ask for help in our [Slack](https://ocf.io/slack),
[Discord](https://ocf.io/discord), [Matrix](https://chat.ocf.berkeley.edu),
[Slack](https://ocf.io/slack), or in person during
[staff hours](https://ocf.io/staffhours)!

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

## Make a pull request!\*
Whenever a technical change to the OCF is made, we use [a pull
request][github-pull-request] on GitHub. Pull requests allow staffers to propose
changes in discrete chunks and get feedback before the code goes live.

You're going to make a pull request to [ocfweb][ocfweb]. Specifically, you'll
add your name to [[the list of everyone who's completed this task|doc
staff/startertasks/completed]].

### Set up
1. Log into [GitHub](https://github.com). If your [[OCF email|doc
   services/mail]] (`<OCF username>@ocf.berkeley.edu`) is not connected to your
   account, [add it to your account emails](https://github.com/settings/emails).
2. Create your personal [fork][github-fork] of [ocfweb][ocfweb].
3. [[Log into supernova|doc staff/procedures/ssh-supernova]].
4. Optional: For easier authentication to GitHub, [generate an SSH
   key][github-ssh-keygen] and [add it to your GitHub account][github-add-key].
   Note: the `xclip` commands will probably not work. Instead, just run `cat
   ~/.ssh/id_rsa.pub` and manually copy it to your clipboard.
5. Return to **your new fork** of ocfweb and [clone the
   repository][github-clone]. Enter your clone with `cd ocfweb`.
6. Take a look at the README. It will tell you to run a few commands to finish
   setting up.

You only have to do this part once. Now that your fork is set up, all future
pull requests to ocfweb will use this same clone.

### Make your change
1. First, you want to create a [new branch][git-branch] to separate this change
   from other changes that you or other people are making. To do this, choose a
   very short name for your branch and run `git checkout -b <branch-name>`. You
   have now created and switched to your new branch.
2. Now, you can edit the file and add your username. Figure out which file
   corresponds to [[the completion list|doc staff/startertasks/completed]] and
   add your username to that file. (Just add the name for now, don't worry about
   adding the URL or brackets.)

   There are a few options for editing the file:
   - If you are familiar with a console text editor like `vim` or `emacs`, you
     can use that to edit the file.
   - If you are using a desktop in the OCF lab, you can use the `~/remote`
     folder on the desktop, which is synced to your home directory on supernova.
   - Other editors may have plugins to let you edit files over SSH, such as [VS
     Code][vscode-remote].
3. Now that you've made the change, check out the README to see how to run
   ocfweb in development mode. Once you're running in dev-mode, navigate to the
   page in your browser and visually check it.
4. Run tests! The instructions for running the tests are also in the README. We
   didn't make any drastic changes, so the tests should hopefully pass without
   any issue.
5. If everything looks good, stage your changes using `git add`, and make a commit
   using `git commit`.
6. Push the change to your fork by running `git push origin <branch-name>`.
7. Return to the GitHub page for your fork. You should see a button to open a
   pull request for the change you just pushed. Go ahead and open that PR!

Once the pull request has been submitted, other OCF staff will have a change to
review your changes and make sure they look good. Once one or two people
approve, the pull request can be merged and your change will go live.

### Update your PR (optional)
Sometimes you will want to update a pull request after it has been created,
because you thought of something new or because another staffer suggested a
change. In this case, you'll update your pull request so that your username on
the list links to the pull request you made.

1. If you have disconnected, log back into supernova and navigate to your ocfweb
   folder.
2. Copy the URL to the GitHub pull request you opened in the last part. Edit the
   list file again, and replace your username with
   `[username](https://link.to/pull/request)`. The brackets and parentheses
   indicate that this is a [link in Markdown][markdown-link], which is the
   markup language we use for the docs.
4. As before, stage your changes and commit them.
5. Optional: Squash your changes. A pull request often will accumulate lots of
   little commits that are not very important. You can "squash" all these
   commits together to make things cleaner.
   1. Run `git rebase -i HEAD~2` (`~2` is the number of commits to rebase) to do an
      "interactive [rebase][git-rebase]" of the last two commits.
   2. A text editor will open with a line for each commit. Leave the first
      commit marked as "pick", but for the second commit, replace "pick" with
      "squash" to squash it into the first one. Save and exit.
   3. You will get a chance to edit the commit message for the squashed commit.
      By default, it just puts the two commit messages together. You might want
      to delete the second message. Save and exit.
   4. You did it! You can run `git log` to check: you should only see one commit
      at the top that is authored by you, instead of two.
6. Push your new changes as before. If you did the optional step, you will have
   to add the argument `--force-with-lease` after `push`.

After pushing, the pull request on GitHub will automatically update with the new
changes.

Congrats on making your PR! If you want to learn more about what you can do with
git, check out our [[documentation on git|doc staff/backend/git]].

[github-pull-request]: https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests
[ocfweb]: https://github.com/ocf/ocfweb
[github-fork]: https://help.github.com/en/github/getting-started-with-github/fork-a-repo
[github-ssh-keygen]: https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key
[github-add-key]: https://help.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account
[github-clone]: https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository
[git-branch]: https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
[vscode-remote]: https://code.visualstudio.com/docs/remote/ssh
[markdown-link]: https://daringfireball.net/projects/markdown/syntax#link
[git-rebase]: https://git-scm.com/book/en/v2/Git-Branching-Rebasing
