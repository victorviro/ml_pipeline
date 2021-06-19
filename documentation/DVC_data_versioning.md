# DVC for data versioning

![](https://i.ibb.co/xLcKZsW/dvc-git.png)

This document shows how we can version a dataset with DVC and Git, and the steps to do it. We are going to go as it would be the first time we use DVC to version the dataset. To see how to version a new dataset in this project, jump to section "Track data".

It's assumed that we have a git repository initialized, a git remote called `origin`, and a dataset file to be versioned in the directory `data/01_raw/data.json`.

### Initialize DVC 

After [installing DVC](https://dvc.org/doc/install), we initialize a DVC project in the current working directory. Note that [`dvc init`](https://dvc.org/doc/command-reference/init) (without flags) expects to run in a Git repository root (a `.git/` directory should be present):

```bash
dvc init
```

A new `.dvc/` directory is created for internal configuration. This directory is automatically staged with `git add`, so it can be easily committed with Git. It contains a specific `.gitignore` file for DVC, a `config` file for configuration (empty for now), and other files.


### Configure storage 

In order to upload DVC-tracked data or models later with `dvc push`, we need to set up a storage. In this example, we add a new google cloud storage (GCS) [data remote](https://dvc.org/doc/command-reference/remote/add) (storage and remote are interchangeable terms in DVC):

```bash
# export GOOGLE_APPLICATION_CREDENTIALS=credentials/GCP_key_file.json
dvc remote add -d storage gs://mcpl/dataset
```

This command creates a remote section in the DVC project's `config` file with the name `storage` and url `gs://mcpl/dataset`. DVC remotes let us store a copy of the data tracked by DVC outside of the local cache, usually a cloud storage service.

**Note**: To use GCS as data storage we need to set the environment variable `GOOGLE_APPLICATION_CREDENTIALS`. More details in [Getting started with authentication in GCP](https://cloud.google.com/docs/authentication/getting-started)

We can list the remotes we have: 

```bash
dvc remote list
```

We commit and push this directory in the git repository:

```bash
git add .dvc/config
git commit -m "Configured DVC remote storage"
git push origin master
```

### Track data

Let's capture the current state of the dataset adding it to DVC tracking (it can be a directory):

```bash
dvc add data/01_raw/data.json
```

DVC stores information about the added file (or directory) in a special `.dvc` metadata file named
`data/01_raw/data.json.dvc`, which is added in the directory of the file (this file is not the dataset itself, it's a metadata file that contains the hash (md5) of the dataset and the path). Later we can convert this file to the dataset. `dvc add` also moved the data to the project's cache `.dvc/cache`, and linked it back to the workspace (the hash or md5 of the file `data.json.dvc` is used to determine the cache path).

**Note**: If the dataset has not changed, dvc does not add it.

Let's commit this file to the git repository:

```bash
git add data/01_raw/data.json.dvc
git commit -m "Added raw data version 1"
git push origin master
```

Now we have the dataset which has been tracked by dvc but the dataset is in our directory and we could want to push it into our remote storage. Now we push the dvc repo to push the data in the remote `storage` we set up earlier (GCS):

```bash
dvc push
```

`dvc push` will copy the data cached locally (in `.dvc/cache`) to the remote storage.

**Note**: If the dataset has been already pushed, this command does nothing. It returns `>> Everything is up to date`.

### Retrieving

Having DVC-tracked data stored remotely, it can be downloaded when it is necessary in this project with `dvc pull` (usually, we run it after clone the git repo with `git clone`, and pulling changes from the git repo with `git pull`). For illustrative purposes, let's remove the dataset (and clear DVC cache) in our directory to show how we can pull it (from the remote storage).

```bash
rm -rf .dvc/cache
rm -f data/01_raw/data.json
```

Now, we can use `dvc pull` to download a new copy of the dataset into our directory (`data/01_raw/data.json`).

### Making changes

When we make a change to a file (or directory), we run `dvc add` again to track the latest version.

```bash
dvc add data/01_raw/data.json
```

Usually, we would also run `git commit` and `dvc push` to save the changes:

```bash
# Using the command line
git add data/01_raw/data.json.dvc
git commit -m "Updated raw data version 2"
git push origin master
```

Now we push the dvc repo to push the data in the remote `storage`:

```bash
dvc push
```

### Switching between versions

The `git checkout` command lets us restore any commit in the repository history (including tags). It automatically adjusts the repo files, by replacing, adding, or deleting them as necessary. To get the previous version of the dataset, we can run:

```bash
git checkout HEAD^1 data/01_raw/data.json.dvc
```
Now, we have the metadata file `data/01_raw/data.json.dvc` from version 1. But the dataset file `data/01_raw/data.json` is still version 2. To update it, we can run 

```bash
dvc checkout
```

Alternatively, we can run `dvc pull`.

### Making more changes and switching between more versions

Suppose we update the dataset again. Now we would have 3 versions of the dataset. 

To get whatever version of the dataset, we can see the git commit hashes associated with these versions (when committing the metadata file `data/01_raw/data.json.dvc`) using `git log` or visually in the commit in the repository manager (GitHub or whatever). Once we have the commit hash of the version we want to go, we do `git checkout hash data/01_raw/data.json.dvc` which will pull the metadata file associated with that version to our repo.

```bash
# Pull the metadata file from the dataset version 1
git checkout 65c3389219389b3cba22c48ac5915bd1 data/01_raw/data.json.dvc
```

To get the dataset, as said previously, we can do `dvc checkout` or `dvc pull`.

**Note**: We can make git tags once we commit a specific version of the dataset (the metadata file). So when switching between versions we can use the name of the tag, instead of the commit hash. An example showing this is available [here](https://dvc.org/doc/use-cases/versioning-data-and-model-files/tutorial).

### References

Info links:

- [DVC  Get Started: Data Versioning](https://dvc.org/doc/start/data-versioning)

- [DVC Tutorial: Data and Model Versioning](https://dvc.org/doc/use-cases/versioning-data-and-model-files/tutorial)

- [DVC user guide](https://dvc.org/doc/user-guide)


### Utils

- Run `dvc diff` to see the files tracked/staged currently.

- Run `dev remove dir_or_file.dvc` to unstage/untrack a file from the dvc repo (and `dvc gc -w` to clear cache).

- [`dvc list <url>`](https://dvc.org/doc/command-reference/list) to list repository contents tracked by DVC and Git.

- [dvc status](https://dvc.org/doc/command-reference/status).