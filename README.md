# download-blocklists

Python script to automatically download blocklist files.

## Disclaimer

Do not use software to engage in illegal sharing of copyrighted material. Downloading copyrighted files without permission is illegal.

## How It Works

This simple python script downloads a compilation of blocklists from the iBlocklist site. A free user can not acccess the combined blocklist file, so this
script automatically downloads the different lists into the Transmission blocklist folder. Finally, the script restarts `transmission-daemon`, which automatically
compiles the various text files into one large blocklist.

## Usage

First, install the following dependencies: `docopt`:

```sh
$ pip install docopt
```

Usage is:

```sh
$ python download_blocklists.py [--f <blocklist-target-folder>]
```

A general use case might be:

```sh
$ python download_blocklists.py
```

To specify the location of your blocklist folder, use the `--f` flag:

```sh
$ python download_blocklists.py
```

## Config

The following optional arguments may be given:

* **--f blocklist-target-folder**: the target folder where your client will look for blocklists. If not set, the script will default to `/var/lib/transmission-daemon/.config/transmission-daemon/blocklists/`
	
* **-v**: show the version number.

* **-h**: show the manual page.

## Automation

This script can be usefully automated to run by using a cronjob.

Open the scheduler in edit mode:

```sh
$ sudo crontab -e
```

Add the cronjob to the bottom of your list. The following example downloads the blocklists at 3am every 5 days. Make sure to point to the correct path to download_blocklists.py.
For help with crontab, follow [this useful link](https://help.ubuntu.com/community/CronHowto).

```sh
0 3 */5 * * /usr/bin/python /usr/local/bin/download_blocklists.py
```

## Dependencies

The following third-party libraries are used:

`docopt`: provides a clean way to generate a help document and accept CLI args;