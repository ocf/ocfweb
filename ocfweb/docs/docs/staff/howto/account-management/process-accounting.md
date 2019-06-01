[[!meta title="Process accounting"]]

Sometimes we want to figure out how resources on a server have been used
recently. For example, we might want to find which user was using tons of CPU
on the web server.

Process accounting lets us look at limited historical data for that. In
particular, process accounting logs what programs have been executed by what
user at what time and for how long. Program arguments are *not* logged, which
is good for helping ensure privacy.

## Useful commands

Some useful commands are below; see `man sa` for many more options.


### List recent commands by user

List programs a user has run, along with timestamps and execution time.

    lastcomm $user


### Show sorted CPU usage of all users (past day)

Shows how much processing time each user has used, sorted by the seventh column
(percentage of CPU minutes).

`re` is real minutes, `cp` is CPU minutes (i.e. the time actually spent
working).

    sa -m -c | sort -n -k 7
