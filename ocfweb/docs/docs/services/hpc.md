[[!meta title="High performance computing"]]

**NOTE: We are in the process of trialing this service to users so that we can
make the service as accommodating and secure as possible. This means that items
concerning the service, including this documentation, are subject to change.
We will do our best to keep everyone updated and notified of changes as they come.**

## Introduction

At the OCF we offer a High Performance Computing (HPC) service for individuals
and groups that need to run computationally demanding software. We currently
have one main HPC server; however, we have plans to expand the cluster to make
use the resources at our disposal.

## Gaining Access

In order to access the HPC cluster, please send an access request to
[help@ocf.berkeley.edu](mailto:help@ocf.berkeley.edu). Make sure to include
your OCF username or [[group account|doc membership#h2_group-accounts]] name
and a detailed technical description of the projects you plan to run on our
HPC infrastructure. This would include information about the nature of the
software being run, as well as the amount of computational resources that are
expected to be needed.

### Connecting

Once you submit your proposal and are approved access you will be able to
connect to our Slurm master node via SSH by running the following command:

```
ssh my_ocf_username@hpcctl.ocf.berkeley.edu
```

If you have trouble connecting please [[contact us|doc contact]] at
[help@ocf.berkeley.edu](mailto:help@ocf.berkeley.edu), or come to
[[staff hours|staff-hours]] when the lab is open and chat with us in person.
We also have a #hpc_users channel on [slack][fco] and [[irc|doc contact/irc]]
where you can ask questions and talk to us about anything HPC.

## The Cluster

Users are currently able to run jobs on our main HPC server, which has 4
1080Ti's and 256GB of DDR4-2400 RAM, which was funded by generous grants from
the Student Tech Fund.

## Slurm

We currently use [Slurm][slurm] as our workload manager for the cluster. We
will soon post technical documentation about our Slurm configuration, but briefly,
Slurm is a free and open-source job scheduler which helps distribute jobs from
all users evenly among HPC computers, referred to as nodes. To use
Slurm there are several commands that will be helpful:

* `srun`: Used to submit jobs.
* `scontrol`: Used to view and edit the Slurm configuration.
* `squeue`: Used to view running and queued jobs.
* `scancel`: Used to cancel jobs.
* `sinfo`: Used to view status of compute nodes in a cluster.

Berkeley Research Computing (BRC) has some useful documentation for using Slurm
[here][brc_slurm], just keep in mind that there are some differences between
their configuration and ours. To put it simply, all of your programs will be
run through Slurm.

## Dependencies
For managing application dependencies, you currently have two options:

### Virtual Environments

First you can use a [virtual environment][venv] if you are using Python
packages. To create a virtual environment navigate to your home directory
and run the following commands:

```
virtualenv -p python3 venv
. venv/bin/activate
```

This will allow you to `pip install` any Python packages that the OCF does not
already have for your program.

### Singularity

For those who need access to non-Python dependencies or have already integrated
their program into Docker, the second option is to use Singularity containers.
[Singularity][singularity] is a containerization platform developed at Lawrence
Berkeley National Laboratory that is designed specifically for HPC environments.
To read more about the benefits of Singularity you can look
[here][singularity_article]. We suggest a particular workflow, which will help
simplify deploying your program on our infrastructure.

#### Installing

We recommend that you do your development on our HPC infrastructure, but you
can also develop on your own machine if you would like. If you are running
Linux on your system, you can install Singularity from the official `apt` repos:

```
sudo apt install singularity-container
```

If you do not have an `apt` based Linux distribution, installation instructions
can be found [here][linux_install]. Otherwise, if you are running Mac you can
look [here][mac_install], or Windows [here][win_install].

#### Building Your Container

```
singularity build --sandbox ./my_container docker://ubuntu
```
This will create a Singularity container named `my_container`. If you are
working on our infrastructure you will *not* be able to install non-pip
packages on your container, because you do not have root privileges.

If you would like to create your own container with new packages, you must
create the container on your own machine, using the above command with
`sudo` prepended, and then transfer it over to our infrastructure.

The `docker://ubuntu` option notifies Singularity to bootstrap the container from
the official Ubuntu docker container on [Docker Hub][docker_hub]. There is also
a [Singularity Hub][singularity_hub], from which you can directly pull
Singularity images in a similar fashion. We also have some pre-built containers
that you may use to avoid having to build your own. They are currently located
at `/home/containers` on the Slurm master node.

#### Using Your Container

```
singularity shell my_container
```
The above command will allow you to shell into your container. By default your
home directory in the container is linked to your real home directory outside
of the container environment, which helps you avoid having to transfer files
in and out of the container.

```
singularity exec --nv my_container ./my_executable.sh
```
This command will open your container and run the `my_executable.sh` script in
the container environment. The `--nv` option allows the container to interface with
the GPU. This command is useful when using `srun` so you can run your program
in a single command.

#### Working on HPC Infrastructure

If you were using a sandboxed container for testing, we suggest you convert it
to a Singularity image file. This is because images are more portable and
easier to interact with than sandboxed containers. You can make this
conversion using the following command:
```
sudo singularity build my_image.simg ./my_sandboxed_container
```

If you were working on the image on your own computer, you can transfer it over
to your home directory on our infrastructure using the following command:
```
scp my_image.simg my_ocf_username@hpcctl.ocf.berkeley.edu:~/
```

To actually submit a Slurm job that uses your Singularity container and runs
your script `my_executable.sh`, run the following command:
```
srun --gres=gpu --partition=ocf-hpc singularity exec --nv my_image.simg ./my_executable.sh
```
This will submit a Slurm job to run your executable on the `ocf-hpc` Slurm
partition. The `--gres=gpu` option is what allows multiple users to run jobs
on a single node so it is important to include. Without it, you will not be
able to interface with the GPUs.

[docker_hub]: https://hub.docker.com/
[singularity_hub]: https://singularity-hub.org/
[singularity_article]: http://www.admin-magazine.com/HPC/Articles/Singularity-A-Container-for-HPC
[slurm]: https://slurm.schedmd.com/
[singularity]: https://singularity.lbl.gov/
[group]: https://www.ocf.berkeley.edu/docs/membership/#h2_group-accounts
[staff_hours]: https://www.ocf.berkeley.edu/staff-hours
[contact]: https://www.ocf.berkeley.edu/docs/contact/
[venv]: https://docs.python.org/3/tutorial/venv.html
[fco]: https://fco.slack.com/
[mac_install]: https://singularity.lbl.gov/install-mac
[win_install]: https://singularity.lbl.gov/install-windows
[linux_install]: https://singularity.lbl.gov/install-linux
[brc_slurm]: http://research-it.berkeley.edu/services/high-performance-computing/running-your-jobs
