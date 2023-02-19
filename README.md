
# Simple Archive

Utility script to store archival data on hetzner storage cloud. Compresses each top level
folder from the source directory individually with zstd and encrypts it with age. Afterwards
the file is uploaded via the upload script (=> can be modified to use other upload methods).

## Usage

```bash
./run.sh --help

age-keygen -o age-key-file

# assume that sftp authentication with ssh keys is already set up
./run.sh archive --source ./src --tempdir /some-local-fast-dir --password-file age-key-file --sftp-host XXXXX.your-storagebox.de --sftp-user XXXX
```

## FAQ

### How to install?

1) Download repository
2) Install requirements: `tar`, `zstd`, `age` (>= 1.0.0), `md5sum`,  `python3`(> 3.8)
    * Often you can just write the command in the shell and the system will tell you what package to install
3) Install python requirements: `pip3 install -r requirements.txt` (pip or pip3, depending on your system)
    * My recommendation would be to use a venv
      environment: `python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt --upgrade`
    * Venv can be activated with `source venv/bin/activate` and deactivated with `deactivate`
4) Run `simple_archive` with `./run.sh --help`

### Why zstd and age?

Both tools are very fast and easy to use. Zstd is a very fast compressor and age is a very
easy to use encryption tool, which is also very fast.
With these tools you can easily achieve >100MB/s compression and encryption speed on relatively 
old hardware (for example Core i5-4670)

