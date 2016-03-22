[[!meta title="Editing docs"]]

The OCF's documentation (formerly known as "the wiki") is a part of the OCF
website built with [Markdown][markdown] where we provide technical support for
users and documentation for fellow staff.

## Overview

Docs is currently a part of the OCF's main website, known as [ocfweb][ocfweb].
Markdown syntax is parsed by [Mistune][mistune] with syntax highlighting done
by [Pygments][pygments].

We use a wiki-like syntax for making links within documentation and the
website, e.g. from [[Virtual Hosting|doc services/vhost#h4_hosting-badge]]:

    All virtual hosts on the OCF must include an [[OCF banner|doc services/vhost/badges]] on the front page that links to the [[OCF home page|home]].

## Editing docs

Edits to the documentation are made via the OCF website's Git repository on
GitHub. The editing process is like our other Git workflows:

1. Fork [the repository on GitHub][ocfweb].

2. Make changes on a new branch.

3. Push your changes.

4. Make a pull request.

Once you make a pull request, it will automatically be tested by
[Jenkins][jenkins], the build server. Jenkins will also deploy your changes
once they have been merged.

For simple changes, you can just click "Edit this Page" in the sidebar. This
will open the file in GitHub, and walk you through the steps for either
commiting on master or making a pull request.

For more complicated ones, the repository's readme file has instructions for
testing and building the website so you can preview your edits before making
the commit. Also see [[our page on Git|doc staff/backend/git]] for further info
on working with OCF repos.


[markdown]: https://daringfireball.net/projects/markdown/syntax
[ocfweb]: https://github.com/ocf/ocfweb
[mistune]: https://github.com/lepture/mistune
[pygments]: http://pygments.org/
[jenkins]: https://jenkins.ocf.berkeley.edu
