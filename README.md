##用法

在git项目里设置sftp属性：

```sh
$ cd git-project
$ git config gfs.sftp.path '/var/www/'
$ git config gfs.sftp.host '1.1.1.1'
$ git config gfs.sftp.port 22
$ git config gfs.sftp.username 'root'
$ git config gfs.sftp.password 'xxxxxx'
```

当有一次新的commit产生后，想将这次的改动上传到服务器:

```sh
$ gfs
```

如果还想同时将改动的文件输出到某个文件夹:

```sh
$ gfs -o 文件夹路径
```
