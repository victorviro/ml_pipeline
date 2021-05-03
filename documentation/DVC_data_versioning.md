# DVC steps

We explain the steps to versioning data with DVC as it was the first time we run the project.

Initialize DVC (after installing it):

```bash
dvc init
```

A new `.dvc/` directory is created for internal configuration. This directory is automatically staged with `git add`, so it can be easily committed with Git. It constains a specific `.gitignore` file for DVC, a `config` file for configuration (empty for now), and other files.


### Configure storage 

In order to upload DVC-tracked data or models later with `dvc push`, we need to setup a storage. In this example, we add a new local [data remote](https://dvc.org/doc/command-reference/remote/add) (or a [google drive storage](https://youtu.be/kLKBcPonMYw?t=205), or a google cloud storage) (storage and remote are interchambiable terms in DVC):

```bash
dvc remote add -d storage /tmp/dvc-storage
dvc remote add -d storage gdrive://1rU99NCYC4WqpCYZcXtyq-WfZJNLh8wGn
# export GOOGLE_APPLICATION_CREDENTIALS=credentials/GCP_key_file.json
dvc remote add -d storage gs://mcpl/dataset
```


This command creates a remote section in the DVC project's `config` file with name `storage` and url `/tmp/dvc-storage` (or `gdrive://1rU99NCYC4WqpCYZcXtyq-WfZJNLh8wGn` or `gs://mcpl/dataset`). DVC remotes let us store a copy of the data tracked by DVC outside of the local cache, usually a cloud storage service.

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

Let's commit this file to the git repository:

```bash
git add data/01_raw/data.json.dvc
git commit -m "Added raw data version 1"
git push origin master
```

Now we have the dataset which has been tracked by dvc but the dataset is in our directory and we could want to push it into our own remote storage. Now we push the dvc repo to push the data in the `storage` directory (`tmp/dvc-storage` or gdrive or GCS)

```bash
dvc push
```
`dvc push` copied the data cached locally (in `.dvc/cache`) to the remote storage we set up earlier (`tmp/dvc-storage` or gdrive or GCS).

### Retrieving

Having DVC-tracked data stored remotely, it can be downloaded when needed in other copies of this project with `dvc pull` (usually, we run it after clone the git repo with `git clone`, and pulling changes from the git repo with  `git pull`).
For learning purposes, let's remove the dataset (and clear DVC cache) in our directory to show how we can pull it (from the remote storage).

```bash
rm -rf .dvc/cache
rm -f data/01_raw/data.json
```

We can use `dvc pull` and that is going to download a new copy of the dataset into our directory (`data/01_raw/data.json`).

### Making changes

When we make a change to a file (or directory), run `dvc add` again to track the latest version.

```bash
dvc add data/01_raw/data.json
```

Usually we would also run `git commit` and `dvc push` to save the changes:

```bash
# Using the command line
git add data/01_raw/data.json.dvc
git commit -m "Updated raw data version 2"
git push origin master
```

Now we push the dvc repo to push the data in the `local_storage` directory.

```bash
dvc push
```

### Switching between versions



### References

Info links:

- [DVC  Get Started: Data Versioning](https://dvc.org/doc/start/data-versioning)

- [DVC Tutorial: Data and Model Versioning](https://dvc.org/doc/use-cases/versioning-data-and-model-files/tutorial)

- [DVC user guide](https://dvc.org/doc/user-guide)


### Utils

- Run `dvc diff` to see the files tracked/staged currently

- Run `dev remove dir_or_file.dvc` to unstage/untrack a file from the dvc repo (and `dvc gc -w` to clear cache)

- [`dvc list <url>`](https://dvc.org/doc/command-reference/list) to list repository contents tracked by DVC and Git

- [dvc status](https://dvc.org/doc/command-reference/status)