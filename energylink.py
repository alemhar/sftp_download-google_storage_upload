import os
import sys
import pysftp
import shutil
from google.cloud import storage
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None


project_id = 'project-id'


sftp_username = 'username'
sftp_userpass = 'password'
sftp_server = "ftp.server.com"
remote_path = "file_directory"
local_path = "c:/local/file/directory"

client = storage.Client(project=project_id)
bucket = client.get_bucket('google_bucket')
blobs = client.list_blobs('google_bucket',prefix='sub_directory/', delimiter='/')


# Get list of current 
bucket_files = []
for blob in blobs:
    bucket_file =blob.name.replace('sub_directory/','') 
    if bucket_file:
        bucket_files.append(bucket_file)



with pysftp.Connection(host=sftp_server, username=sftp_username, password=sftp_userpass, cnopts=cnopts) as sftp:
    print("Connection succesfully stablished ... ")

    # Switch to a remote directory
    sftp.cwd(remote_path)

    # Obtain structure of the remote directory 
    directory_structure = sftp.listdir_attr()

    for attr in directory_structure:
        if attr.filename in bucket_files:
            print ('Skip download, file exist: ' + attr.filename)
            
        else:
            print ('Downloading: ' + attr.filename)
            sftp.get('/' + remote_path + '/' + attr.filename, local_path + '/' + attr.filename)


# loop in local download directory
for root, dirs, files in os.walk(local_path):   
    for basename in files:
        # copy file to bucket    
        # move file to archive folder
        # delete file from download folder
        

        blob = bucket.blob('xls/' + basename)
        blob.upload_from_filename('c:/local/file/directory/' + basename)

        file_des = 'c:/local/file/archive/' + basename    
        file_src = 'c:/local/file/directory/' + basename
        shutil.move(file_src, file_des)
        
print ('Completed.')
