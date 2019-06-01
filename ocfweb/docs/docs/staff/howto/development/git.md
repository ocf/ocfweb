[[!meta title="Git"]]


Git is a distributed revision control system used by the OCF. Other version
control systems include Mercurial (also distributed) and Subversion (not
distributed).

## Workflow

Although Git is a great tool for large-scale distributed development, for us a
Subversion-like workflow with a "central repository" (where you clone/fetch
from and push to) and linear history makes more sense. The instructions below
assume that development is happening in a single branch.

**Only commit your own, original work**.  You may commit another staff member's
work if you have permission and change the author appropriately (e.g.,
`--author="Guest User <guser@ocf.berkeley.edu>"`). When committing, `git config
user.name` should be your name and `git config user.email` should be your OCF
email address -- this should be taken care of by [[LDAP|doc
staff/backend/ldap]] and `/etc/mailname` on OCF machines.

### To "update"

Get the latest commits from the central repository and update your working
tree.

    git pull --rebase

This will `git fetch` (update your local copy of the remote repository) and
`git rebase` (rewrite current branch in terms of tracked branch). The rebase
prevents unnecessary merge commits by moving your local commits on top of the
latest remote commit (`FETCH_HEAD`). This is a good thing if you have any local
commits which have not yet been pushed to the remote repository.

If you have "dirty" uncommitted changes, you'll need to commit them or stash
them before rebasing (`git stash`).

### To "upload"

Make commits and push them to the central repository.

    git add FILES # add current state of FILES in working tree to index
    git commit    # store index as a commit in current branch
    # repeat git add and git commit for more commits
    git rebase -i # clean up the history (reword or squash commits)
    git push      # push current branch to tracked branch in remote repository

Use `git add -p` to inspect individual changes before adding each one to the
index, and `git commit -v` to show a diff of your commit when you are prompted
for a commit message.

If commits have been made on the remote repository in the meantime, you'll need
to "update" first (see above).

### To "import"

Pull someone else's changes into the central repository, for example from a
branch in a staff member's repository (`REMOTE`).

    git fetch REMOTE                             # update local copy of remote
    git log --graph --decorate FETCH_HEAD ^HEAD^ # list remote commits on top of current branch
    git diff FETCH_HEAD                          # compare current branch with remote branch
    git merge --ff-only FETCH_HEAD               # merge in if can linearly fast-forward

If you can't fast-forward merge, "update" the remote repository first (see
above).

If you want a merge commit, you can `git merge --no-ff` instead.

## Other useful commands

Current state of working tree:

    git status

Throw away uncommitted changes:

    git checkout -- FILES  # in particular files
    git reset --hard HEAD # in the entire working tree

Revise the last commit:

    git commit --amend

Undo the last commit:

    git reset HEAD^        # leaves changes in the working tree so they can be committed again
    git reset --hard HEAD^ # throws away changes

File operations:

    git mv
    git rm

Advanced:

    git filter-branch # rewrite history according to a filter
    git blame         # show the commit which last modified each line of a file
    git reflog        # useful for undoing git mistakes

## Terminology

* branch
  * line of changes in a repository, default branch is `master`
* fast-forward
  * advance branch forward in a linear sequence
  * this is usually what we want: the new commit builds directly on the
    previous commit
* hooks
  * optional scripts that can be executed during git operations
  * for example, validate syntax before accepting a commit or deploy code to a
    server
* index (aka staging area)
  * files that are ready to be stored in your next commit
* references (aka refs)
  * SHA-1 hashes that identify commits
  * `HEAD` points to the latest commit ref in the current branch (`HEAD^` to
    the one before it)
* remote
  * upstream repository that you can `git fetch` from or `git push` to, default
    is `origin`
  * local branches can "track" remote branches (e.g., `master` tracking
    `origin/master`)
* working tree (aka workspace or working directory)
  * directory that checked out files reside
  * this includes the current branch and any "dirty" uncommitted changes
    (staged or not)

## Recommended reading

* [A Visual Git Reference](https://marklodato.github.io/visual-git-guide/)
* [Git Immersion](http://www.gitimmersion.com/)
* [The Case for Git Rebase](http://darwinweb.net/articles/the-case-for-git-rebase)
