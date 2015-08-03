#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ssh,os,time,commands,sys,getopt

localPatch=''
is_from_cached=False
is_to_remote=False

opts,args=getopt.getopt(sys.argv[1:],"rco:")
for op,value in opts:
    if op=="-o":
        localPatch=os.path.abspath(value)
    elif op=='-c':
        is_from_cached=True
    elif op=='-r':
        is_to_remote=True


gitWorkTree=os.popen("pwd").readline().strip('\n')
os.popen("GIT_WORK_TREE="+gitWorkTree)
patchFile=str(time.time())+".tar.gz"
patchPath="/tmp/"+patchFile

if is_from_cached ==False:
    comm="git archive -o "+patchPath+" HEAD $(git diff --name-only HEAD^ HEAD)"
else:
    comm="tar -zcvf "+patchPath+" $(git diff --cached --name-status | grep '^D' -v | sed 's/A\t//g' | sed 's/M\t//g')"
(status, output) = commands.getstatusoutput(comm)
if(status!=0):
    print status,output
    exit()

print "Patch file is: "+patchPath

#opts,args=getopt.getopt(sys.argv[1:],"o:")
#for op,value in opts:
#    if op=="-o":
#        localPatch=os.path.abspath(value)
if localPatch != '':
    (status, output) = commands.getstatusoutput("cd "+localPatch+" && tar -zxf "+patchPath)
    if(status!=0):
        print status,output
        exit()
    else:
        print "Copy to local folder: "+localPatch

if is_to_remote==True:
    (status, output) = commands.getstatusoutput("git config --get gfs.sftp.path")
    if(status!=0):
        print status,output
        print "Config gfs.sftp.path doesn't exist"
        exit()
    GFS_SFTP_PATH=output

    (status, output) = commands.getstatusoutput("git config --get gfs.sftp.host")
    if(status!=0):
        print status,output
        print "Config gfs.sftp.host doesn't exist"
        exit()
    GFS_SFTP_HOST=output

    (status, output) = commands.getstatusoutput("git config --get gfs.sftp.port")
    if(status!=0):
        print status,output
        print "Config gfs.sftp.port doesn't exist"
        exit()
    GFS_SFTP_PORT=int(output)

    (status, output) = commands.getstatusoutput("git config --get gfs.sftp.username")
    if(status!=0):
        print status,output
        print "Config gfs.sftp.username doesn't exist"
        exit()
    GFS_SFTP_USERNAME=output

    (status, output) = commands.getstatusoutput("git config --get gfs.sftp.password")
    if(status!=0):
        print status,output
        print "Config gfs.sftp.password doesn't exist"
        exit()
    GFS_SFTP_PASSWORD=output

    client=ssh.SSHClient()
    client.set_missing_host_key_policy(ssh.AutoAddPolicy())
    client.connect(GFS_SFTP_HOST, port=GFS_SFTP_PORT, username=GFS_SFTP_USERNAME, password=GFS_SFTP_PASSWORD)

    sftp=client.open_sftp()
    stdin, stdout, stderr = client.exec_command("cd "+GFS_SFTP_PATH)
    stdout.read()



    sftp.put(patchPath,GFS_SFTP_PATH+patchFile)

    stdin, stdout, stderr = client.exec_command("cd "+GFS_SFTP_PATH+" && tar -zxf "+GFS_SFTP_PATH+patchFile  )
    print stdout.read()
    stdin, stdout, stderr = client.exec_command("rm "+GFS_SFTP_PATH+patchFile)
    print stdout.read()

    print "Update success!"
