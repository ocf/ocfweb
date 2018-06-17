[[!meta title="High Performance Computing"]]

**NOTE: We are in the process of trialling this service to users so that we can make the service as accommodating and secure as possible. This means that items concerning the service, including this documentation, are subject to change. We will do our best to keep everyone updated and notified of changes as they come.**

## Introduction

At the OCF we offer a High Performance Computing (HPC) service for individuals and groups that need to run computationally demanding software. Our main HPC server is currently named `corruption`, however we also have plans to expand the cluster to maximize the use of the resources at our disposal.

### Gaining Access

In order to access the HPC cluster, you must send a proposal to [help@ocf.berkeley.edu](mailto:help@ocf.berkeley.edu). Make sure to include your OCF username or group account name and a short, but detailed technical description of the experiments you plan to run on our HPC infrastructure. This would include information about the nature of the software being developed, as well as the amount of computational resources that are expected to be needed.

#### Connecting

Our Slurm master node is currently `segfault`. Once you submit your proposal and are approved access you will be able to connect via ssh by running the following command:

    ssh my_ocf_username@segfault.ocf.berkeley.edu

If you have trouble connecting please email us at [help@ocf.berkeley.edu](mailto:help@ocf.berkeley.edu).

### The Cluster

Users currently have access to our main HPC server `corruption`, which has the following specifications:

* 2x NVIDIA GTX 1080 Ti
* 1x Intel Intel(R) Xeon(R) CPU E5-2640 v4
* 4x 16Gb ECC DDR4-2400 ram

We have also recently been approved a grant that will be awarded in the coming weeks. So in addition to the above, the following will be installed in `corruption`:

* 2x NVIDIA GTX 1080 Ti
* 1x Intel Intel(R) Xeon(R) CPU E5-2640 v4
* 12x 16Gb ECC DDR4-2400 ram

### Slurm

We currently use [Slurm][slurm] as our workload manager for the cluster. We will soon post technical documentation about our Slurm configuration, but briefly, Slurm is a free and open-source job scheduler which helps manage multi-user use of distributed computational resources, referred to as nodes. In short, all of your programs will be run through Slurm. To use Slurm there are several commands that will be helpful:

* `srun`: Used to submit jobs.
* `scontrol`: Used to view and edit the Slurm configuration.
* `squeue`: Used to view running and queued jobs.

### Dependencies
For managing application dependencies, one currently has two options:

First you could use a virtual environment if you are using Python packages. To create a virtual environment navigate to your home directory and run the following commands

    virtualenv -p python3.5 venv
    . venv/bin/activate

This will allow you to *pip install* any Python packages that the OCF does not already have for your program.

For those who need access to non-python dependencies or have already integrated their program into Docker, the second option is to use Singularly containers. [Singularity][singularity] is a containerization platform developed at Laurence Berkeley National Laboratory that is designed specifically for HPC environments. To read more about the benefits of Singularity you can look [Here][singularity_article]. Using a container is quite simple, below are a few commands to help getting started.

1. `singularity build --sandbox ./my_container docker://ubuntu`: This will create a Singularity container named `my_container`. It is important that you use the `--sandbox` option, since this is the only way that you can build a container without root privileges. The `docker://ubuntu` option notifies singularity to bootstrap the container from the official Ubuntu docker container on [Docker Hub][docker_hub]. There is also a [Singularity Hub][singularity_hub], from which you can directly pull Singularity images in a similar fashon. We also have some pre-built containers that you may use to avoid having to build your own. They are currently located at `/home/containers`.

2. `singularity exec --nv my_container ./my_executable.sh`: This will open your container and run the `my_executable.sh` script in the container environment. The --nv option allows the container to interface with the GPU. This command is useful when using `srun` so you can run your program in a single command.

3. `srun -p ocf-hpc singularity exec --nv my_container ./my_executable.sh`: This will submit a Slurm job to run your executable on the `ocf-hpc` Slurm parition.

[docker_hub]: https://hub.docker.com/
[singularity_hub]: https://singularity-hub.org/
[singularity_article]: http://www.admin-magazine.com/HPC/Articles/Singularity-A-Container-for-HPC
[slurm]: https://slurm.schedmd.com/
[singularity]: https://singularity.lbl.gov/
