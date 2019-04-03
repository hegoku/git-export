## Install

Copy `git-export.py` to a folder:

```sh
$ cp git-export.py ~/
```

Edit `~/.bashrc` to add alias:

```sh
alias git-export='/home/xx/git-export.py'
```

or to include PATH:

```sh
PATH=$PATH:/home/xx
```

## How to use

Setting sftp configs in git project:

```sh
$ cd git-project
$ git config gep.sftp.path '/var/www/'
$ git config gep.sftp.host '1.1.1.1'
$ git config gep.sftp.port 22
$ git config gep.sftp.username 'root'
$ git config gep.sftp.password 'xxxxxx'
```

`git-export` has three options:

```
-r upload to server
-c choose staging area
-o path_of_folder export files to local folder
```

Just want to pack changes from new commit:

```sh
$ git-export
Patch file is: /tmp/xxx.tar.gz
```

then it will pack changes to `/tmp/xxx.tar.gz`

Just want to pack changes from staging area:

```sh
$ git-export -c
Patch file is: /tmp/xxx.tar.gz
```

To upload files added or modified in new commmit to server:

```sh
$ git-export -r
```

Both uploading new commit to server and exporting these files to local folder:

```sh
$ git-export -ro path_of_folder
```

To upload files added or modified in staging area to server:

```sh
$ git-export -cr
```

To export modified files between two commits:

```sh
$ git-export -o path_of_folder 0df32f 430fds
```

To export modified files from one commit:

```sh
$ git-export -o path_of_folder 0df32f
```
