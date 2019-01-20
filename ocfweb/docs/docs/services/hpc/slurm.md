[[!meta title="Slurm"]]

## Slurm

In order to use the resources of our HPC computng nodes, you must submit your computing tasks through [Slurm][slurm], which will ensure that your task, or job, is given exclusive access to some CPUs, memory, and GPUs if needed. Slurm also intelligently queues jobs from different users to most efficiently use our nodes' resources.

## Running a job through Slurm

Submitting a job to Slurm can be done in one of two ways: through `srun`, and through `sbatch`.

When using `srun`, options are supplied using command-line flags, and the job is attached to the terminal you run `srun` from. If there is a queue to run jobs, the terminal will wait until your job starts running, and if the terminal closes, the job will be cancelled.

By contrast, to submit a job using `sbatch`, you must first create a batch file that includes options for your job, and the commands that your job will run. The batch file is then submitted, and after the job runs, log files with the job's output to `stdout` are put into your home directory.

#### When to use `srun` versus `sbatch`

If your job requires interactivity or inputs from the terminal, or you need a terminal to test or experiment, use `srun`. Otherwise, use `sbatch`, as you don't have to keep your terminal open until the job runs.

### Resource options

*Some terminology:* Slurm refers to a process as a "task". Even if a single process is using multiple threads/CPUs, it still counts as one task.

**By default, without any flags, a job you submit will be allocated one CPU, 100 MB of RAM, and no GPUs, and will run for at maximum 2 days. In order to allocate more resources and time to your job, you must set one or more of these flags:**

* `-n` / `--ntasks`:
    - The number of tasks/processes to allocate. **Default is 1.**
* `-c` / `--cpus-per-task`:
    - The number of CPUs to allocate per task. **Default is 1.**
* `--mem`:
    - The total amount of RAM to allocate. By default, the number supplied is assumed to megabytes. However, the prefixes `K`, `M`, `G`, and `T` can be appended to the number instead. For example, to allocate 5 gigabytes of ram, use `--mem=5G`. **Default is 100 megabytes.**
* `--gres` **(Optional)**:
    - Allocates some GPUs to your job. The format is `--gres=gpu:[optional type]:[number to allocate]`. For example, to allocate 2 GPUs of any type, you would include `--gres=gpu:2`. To allocate two Nvidia 1080Ti GPUs (our only type right now), you would include `--gres=gpu:nv1080:2`. **No default.**
* `--t` / `--time` **(Optional)**:
    - The maximum amount of time your job can take before Slurm forcefully kills it. Acceptable time formats include "minutes", "minutes:seconds", "hours:minutes:seconds", "days-hours", "days-hours:minutes" and "days-hours:minutes:seconds". You cannot set the time limit greater than the **default, which is 2 days.**

### Using `srun`

On `hpcctl`:

```
srun [command-line flags] [command to run]
```

For example, to run a job that uses 4 CPUs, 8 GB of RAM, and 1 GPU:

```
bzh@hpcctl:~$ srun --ntasks=1 --cpus-per-task=4 --mem=8G --gres=gpu:1 echo "Hello world!"

Hello world!
```

#### Running an interactive terminal

To start up an interactive terminal on a compute node, use the `--pty [your terminal of choice]` flag. For most everyone, you'll be using `bash`, so to start an interactive terminal on a node, run:

```
srun [other command-line flags] --pty bash
```

### Using `sbatch`

A Slurm batch script is functionally the same as a regular `bash` script: The `bash` shebang at the start, and script after.

However, to pass options into SLURM, you'll need to add some special comment lines, which are in the format `#SBATCH [command-line flag]=[value]`. **They must be after the shebang but before any non-comments**.

For example, a batch script which uses 4 CPUs, 8 GB of RAM, and 1 GPU has its contents as:

```
 #!/bin/bash
 #SBATCH --ntasks=1
 #SBATCH --cpus-per-task=4
 #SBATCH --mem=8G
 #SBATCH --gres=gpu:1

 echo "Hello world!"
```

You submit batch scripts to Slurm with:

```
sbatch [path to batch script]
```

#### Output from `sbatch`

By default, output from your job (`stdout` and `stderr`) is placed into a file in the directory you ran `sbatch` from. it will be named `slurm-[your job's numeric ID].out`.

To specify a different output file, use the `-o` / `--output` flag. For example, to redirect output to a file named `job.log` in your home directory, use `--output=~/job.log`.

#### Cancelling a job

To cancel your job before it's run, run `scancel [job ID]`. Your job's ID is output when a batch script is submitted, or you can find it using `squeue` (more details below).

## Viewing Slurm info

To view the queue of running and pending jobs from all users, run `squeue`. To see the details of one job, run `squeue -j [job ID]`.

To view the list of all HPC nodes, and some details about them, run `sinfo -N -l`.

[slurm]: https://slurm.schedmd.com/
