# DVC steps

We explain the steps to versioning data with DVC as this is the first time we run the project.

Initialize DVC (after installing it):

```bash
dvc init
```

A new `.dvc/` directory is created for internal configuration. This directory is automatically staged with `git add`, so it can be easily committed with Git. It constains a specific `.gitignore` file for DVC, a `config` file for configuration (empty for now), and other files.


In order to upload DVC-tracked data or models later with `dvc push`, we need to setup a storage. In this example, we add a new local [data remote](https://dvc.org/doc/command-reference/remote/add) (storage and remote are interchambiable terms in DVC):

```bash
dvc remote add -d local_storage /tmp/dvc-storage
```
This command creates a remote section in the DVC project's `config` file with name `local_storage` and url `/tmp/dvc-storage`. DVC remotes let us store a copy of the data tracked by DVC outside of the local cache, usually a cloud storage service (local storage in our case).

We can list the remotes we have: 

```bash
dvc remote list
```

We commit and push this directory in the git repository (via command line or vscode):
```bash
# Using the command line
git add .dvc/config
git commit -m "Configure remote storage"
```

Let's capture the current state of the dataset adding it to DVC tracking (it can be a directory):
```bash
dvc add data/01_raw/Data_test.json
```

DVC stores information about the added file (or directory) in a special `.dvc` metadata file named
`data/01_raw/Data_test.json.dvc`, which is added in the directory of the file (this file is not the dataset itself, it's a metadata file that contains the hash (md5) of the dataset and the path). Later we can convert this file to the dataset. `dvc add` also moved the data to the project's cache `.dvc/cache`, and linked it back to the workspace (the hash or md5 of the file `Data_test.json.dvc` is used to determine the cache path).

Let's commit this file to the git repository (with vscode or with the command line):

```bash
# Using the command line
git add data/01_raw/Data_test.json.dvc
git commit -m "Added raw data (max_char_per_line raw data)"
# git push
```

Now we have the dataset which has been tracked by dvc but the dataset is in our directory and we could want to push it into our own remote storage. Now we push the dvc repo to push the data in the `local_storage` directory (`tmp/dvc-storage`)

```bash
dvc push
```
`dvc push` copied the data cached locally (in `.dvc/cache`) to the remote storage we set up earlier (`tmp/dvc-storage`).

### Retrieving

Having DVC-tracked data stored remotely, it can be downloaded when needed in other copies of this project with `dvc pull` (usually, we run it after clone the git repo with `git clone`, and pulling changes from the git repo with  `git pull`.
For learning purpose, let's remove the dataset (and clear DVC cache) in our directory to show how we can pull it (from the remote storage).

```bash
rm -rf .dvc/cache
rm -f data/01_raw/Data_test.json
```

We can use `dvc pull` and that is going to download a new copy of the dataset into our directory (`data/01_raw/Data_test.json`).

### Making changes

When we make a change to a file (or directory), run `dvc add` again to track the latest version.

```bash
dvc add data/01_raw/Data_test.json
```

Usually we would also run `git commit` and `dvc push` to save the changes:

```bash
# Using the command line
git add data/01_raw/Data_test.json.dvc
git commit -m "Updated raw data (max_char_per_line raw data)"
# git push
```


```bash
dvc push
```

### Switching between versions



## References

Info links:

- [dvc Get Started: Data Versioning](https://dvc.org/doc/start/data-versioning)

- [`dvc list <url>`](https://dvc.org/doc/command-reference/list)

- [dvc status](https://dvc.org/doc/command-reference/status)


## Utils

- Run `dvc diff` to see the files tracked/staged currently.

- Run `dev remove dir_or_file.dvc` to unstage/untrack a file from the dvc repo (and `dvc gc -w` to clear cache).