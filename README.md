# UOCloud sync
Transfer files from UOCloud provisionable storage to Talapas, via Globus.

### Motivation
Storage on Talapas is expensive, and UOCloud storage is cheaper, but it is a pain
to transfer files from the cheaper storage using Globus because you first have
to open the web app and authenticate, then start a transfer, then you get
emailed sometime later when the transfer finishes. Wouldn't it be nice to have
a program do that for you?

### Setup
First, [create two Globus shares](https://docs.globus.org/how-to/share-files/), one
for the UOCloud storage and one for the Talapas storage. The shares have to be shared with
the identity associated with the `uocloud_sync` app, b2e31a30-19bb-4ac1-9617-6dcac0f6cff8@clients.auth.globus.org. Remember the "Share Display Name".

Then a configuration file containing a Globus client ID and secret need to copied to where the app will run.

Then, run `uocloud_sync`.

### Usage
```
uocloud_sync.py --src SRC_SHARE:PATH --dest DEST_SHARE:PATH
```
- `SRC_SHARE` is the name of the source Globus endpoint to copy from. For example, "SANLab Warm Storage".
- `PATH` is the source directory to copy. For example
- `DEST_SHARE` is the name of the destination Globus endpoint to copy to. For example, "SANLab Talapas share". This share points to /projects/sanlab/shared on Talapas.
- `PATH` is the destination directory name.

Example usage:
- To transfer the `Devaluation\output` directory from UOCloud storage, to Talapas, creating a new directory in `/projects/sanlab/shared/Dev_temp`:
```
uocloud_sync.py --src "SANLab Warm Storage:/Devaluation/output" --dest "SANLab Talapas share:/Dev_temp"

    Waiting for transfer to complete with task_id: fd1a44d2-6fb1-11ea-960e-0afc9e7dd773
    /Devaluation/output/DEV004_run1_16-Apr-2018_19-18.mat -> /Dev_temp/DEV004_run1_16-Apr-2018_19-18.mat
    /Devaluation/output/DEV004_run2_15-May-2018_18-41.mat -> /Dev_temp/DEV004_run2_15-May-2018_18-41.mat
    /Devaluation/output/DEV004_run3_03-Sep-2018_12-48.mat -> /Dev_temp/DEV004_run3_03-Sep-2018_12-48.mat
    /Devaluation/output/DEV004_run4_15-Nov-2018_18-04.mat -> /Dev_temp/DEV004_run4_15-Nov-2018_18-04.mat
    ...
```

#### Use case
In a slurm job, transparently copy data before analysis, perform the analysis, then copy the results to cheaper storage and clean up / delete on Talapas. For example, in a SBATCH script:
```
#!/bin/bash
#SBATCH --account=dcnlab
#SBATCH --partition=ctn
#SBATCH --job-name=cpac
#SBATCH --output=cpac_sub-DEV107.out
#SBATCH --error=cpac_sub-DEV107.err
#SBATCH --time=8-00:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --cpus-per-task=4

# Get data onto Talapas
SRC_PATH="sub-ABC999"
DEST_PATH="/cpac/analysis"
module load python3
uocloud_sync.py --src UOCloud_share:$SRC_PATH --dest Talapas_share:$DEST_PATH

# Run analysis
module load singularity
singularity run /projects/dcnlab/shared/FP/containers/C-PAC_1.6.1.sif

# Transfer data back to UOCloud
uocloud_sync.py --src Talapas_share:$DEST_PATH --dest UOCloud_share:$SRC_PATH

# Clean up on Talapas
rm -rf $DEST_PATH
```
