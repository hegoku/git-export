#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import paramiko as ssh,os,time,commands,sys,getopt

localPatch=''
is_from_cached=False
is_to_remote=False
old_commit='HEAD^'
new_commit="HEAD"

opts,args=getopt.getopt(sys.argv[1:],"hrco:")
for op,value in opts:
    if op=="-o":
        localPatch=os.path.abspath(value)
    elif op=='-c':
        is_from_cached=True
    elif op=='-r':
        is_to_remote=True
    elif op=='-h':
        print "usage: git-export.py -h  show usage"
        print "   or: git-export.py [-r] [-c] [-o <dir>]"
        print "   or: git-export.py [-r] [-o <dir>] <commit>"
        print "   or: git-export.py [-r] [-o <dir>] <old_commit> <new_commit>"
        print ""
        print "   -r\t\t upload to server"
        print "   -c\t\t choose staging area"
        print "   -o <dir>\t export files to local folder"
        print ""
        exit()

gitWorkTree=os.popen("pwd").readline().strip('\n')
os.popen("GIT_WORK_TREE="+gitWorkTree)
patchFile=str(time.time())+".tar.gz"
patchPath="/tmp/"+patchFile

if is_from_cached ==False:
    if(len(args)==1):
        old_commit=args[0]+"^"
        new_commit=args[0]
    elif(len(args)==2):
        old_commit=args[0]
        new_commit=args[1]
    #comm="git archive -o "+patchPath+" HEAD $(git diff --name-status HEAD^ HEAD | grep '^D' -v | sed 's/A\t//g' | sed 's/M\t//g' | sed 's/^/&\'/g' | sed 's/$/&\'/g')"
    (status, output) = commands.getstatusoutput("echo $(git diff --name-status "+old_commit+" "+new_commit+" | grep '^D' -v | sed 's/A\t//g' | sed 's/M\t//g' | sed 's/^/\"/g' | sed 's/$/\"/g')")
    #comm="tar -zcvf "+patchPath+" "+output
    comm="git archive -o "+patchPath+" "+new_commit+" "+output
else:
    (status, output) = commands.getstatusoutput("echo $(git diff --cached --name-status | grep '^D' -v | sed 's/A\t//g' | sed 's/M\t//g' | sed 's/^/\"/g' | sed 's/$/\"/g')")
    comm="tar -zcvf "+patchPath+" "+output
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
    (status, output) = commands.getstatusoutput("git config --get gep.sftp.path")
    if(status!=0):
        print status,output
        print "Config gep.sftp.path doesn't exist"
        exit()
    GEP_SFTP_PATH=output

    (status, output) = commands.getstatusoutput("git config --get gep.sftp.host")
    if(status!=0):
        print status,output
        print "Config gep.sftp.host doesn't exist"
        exit()
    GEP_SFTP_HOST=output

    (status, output) = commands.getstatusoutput("git config --get gep.sftp.port")
    if(status!=0):
        print status,output
        print "Config gep.sftp.port doesn't exist"
        exit()
    GEP_SFTP_PORT=int(output)

    (status, output) = commands.getstatusoutput("git config --get gep.sftp.username")
    if(status!=0):
        print status,output
        print "Config gep.sftp.username doesn't exist"
        exit()
    GEP_SFTP_USERNAME=output

    (status, output) = commands.getstatusoutput("git config --get gep.sftp.password")
    if(status!=0):
        print status,output
        print "Config gep.sftp.password doesn't exist"
        exit()
    GEP_SFTP_PASSWORD=output

    client=ssh.SSHClient()
    client.set_missing_host_key_policy(ssh.AutoAddPolicy())
    client.connect(GEP_SFTP_HOST, port=GEP_SFTP_PORT, username=GEP_SFTP_USERNAME, password=GEP_SFTP_PASSWORD)

    sftp=client.open_sftp()
    stdin, stdout, stderr = client.exec_command("cd "+GEP_SFTP_PATH)
    stdout.read()



    sftp.put(patchPath,GEP_SFTP_PATH+patchFile)

    stdin, stdout, stderr = client.exec_command("cd "+GEP_SFTP_PATH+" && tar -zxf "+GEP_SFTP_PATH+patchFile  )
    print stdout.read()
    stdin, stdout, stderr = client.exec_command("rm "+GEP_SFTP_PATH+patchFile)
    print stdout.read()

    print "Update success!"
