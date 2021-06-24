<div align="center">
<h1>Nerd-Storage</h1>
</div>

![](https://raw.githubusercontent.com/0xHaru/Nerd-Storage/master/media/screenshot.png)

A simple LAN storage.

## Description

Nerd-Storage is a simple web server for sharing files on the local network.

It supports the download of files and directories, the upload of multiple files at once, making a directory, updates and deletions.

The user can also upload an existing directory as a .zip file which will then be extracted inside the storage as a folder.

## Prerequisites

-   Linux

-   Python 3.6+

## Dependencies

`pip install Flask && pip install Flask-Login && pip install Jinja2`

-   [Flask](https://pypi.org/project/Flask/)

-   [Flask-Login](https://pypi.org/project/Flask-Login/)

-   [Jinja2](https://pypi.org/project/Jinja2/)

## Installation

`pip install Nerd-Storage`

## Usage

Run: `nerdstorage`

To access the storage go to: `http://<server-local-ip-addr>:5000/`

To print help information: `nerdstorage --help`

## Configuration

1. Run `hash.py` to set the login password.
2. Edit `config.py` to set the storage path.

This command will output the full path of `hash.py` and `config.py`:

`pip show Nerd-Storage | grep 'Location' | grep -o -E '[/].+' | xargs -I@ printf '@/NERD/hash/hash.py\n@/NERD/config.py\n'`

## Known Issues

1. If your `/tmp` is too small, change it in `/etc/fstab` by following the steps in the section below.
2. If a file is uploaded that is larger than the amount of RAM available on the host machine, the host machine will crash. This is believed to be an error in the [Werkzeug](https://github.com/pallets/werkzeug) module (a [Flask](https://github.com/pallets/flask) dependency). We are currently investigating this and trying to find a monkey patch or a fix. Internal developers on the [Pallets Team](https://github.com/pallets) have been informed and are aware of the issue.

## Fixing /tmp Size in /etc/fstab

Editing `/etc/fstab` can be done with Vim, Nano, GEdit, etc. but _must_ be run as **sudo**.

This is an example with nano: `sudo nano /etc/fstab`
Note: it may be slightly different on different machines, but the core concept is the same; look for `/tmp` or `tmpfs`.

Each line in `/etc/fstab` follows this format: `<file system> <dir> <type> <options> <dump> <pass>`

You will find the line: `tmpfs /tmp tmpfs defaults,noatime,mode=1777 0 0`

and append a `size=10G` after the `defaults`, making the new line:

`tmpfs /tmp tmpfs defaults,size=10G,noatime,mode=1777 0 0`

and Save and Close the file, then reboot the system.

## CLI

[nerdcli](https://github.com/0xHaru/Nerd-Storage/blob/master/cli/nerdcli.sh) is a command line interface for Nerd-Storage.

Useful link for newbies: [unix.stackexchange.com/questions/storing-shell-scripts](https://unix.stackexchange.com/questions/201768/storing-shell-scripts)

```
usage: nerdcli [--parameter]

--login                         login
--logout                        logout
--ls PATH                       list directory content
--download PATH                 download file or directory
--mkdir PATH                    make a directory
--upload PATH FILE_PATH         upload a file
--upload-dir PATH FILE_PATH     upload a .zip as a directory
--delete PATH                   delete a file or directory

Config:
        Set IP and PORT.
        Script path: /path/to/script

Examples:
        https://github.com/0xHaru/Nerd-Storage/blob/master/cli/examples.md

Project home page: https://github.com/0xHaru/Nerd-Storage
```

## Demo

Release 0.0.9

![](https://raw.githubusercontent.com/0xHaru/Nerd-Storage/master/media/demo.gif)

## License

This project uses the following license: [GPLv3](https://github.com/0xHaru/Nerd-Storage/blob/master/LICENSE).
