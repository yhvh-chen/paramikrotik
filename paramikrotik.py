# Author: yhch_chen
# Update: 17/08/2021
# License: Apache2.0

import paramiko
import pandas as pd
import jinja2
import os
import time

# Connection name
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# Establish connection function
def connect_host(host, user, passwd):
    #print('- connecting host', 20 * '>')
    client.connect(host, username=user, password=passwd)
# Disconnection Function
def close_host():
    #print('- closing host', 20*'>')
    client.close()

# Send commands from xlsx file
class send_commd:
    def __init__(self, host, user, passwd, commSheet):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.commSheet = commSheet
# Send TS command in tsFile's sheet
    def tb_shoot(self):
        tsFile = 'pmtk_comm.xlsx'

        # command = {'Address infomation': 'ip add print',
        #            'Interfaces infomation': 'interface print detail terse'
        #            }
        # print('- reading file', 20 * '>')

        print('- Trouble Shooting '+ self.host, 20 * '>')
# Read xlsx into a dict
        if os.path.exists(tsFile):
            df = pd.read_excel(tsFile, sheet_name=self.commSheet)
            df.dropna(inplace=True)
            fileCommand = df.set_index('Function').to_dict()['Command']
            #for k, v in command.items():
            for k, v in fileCommand.items():
                print('\n', 10 * '-', k, 10 * '-', '\n')
# Use other function send command
                self.exce(v)
        else:
            print('- ERROR: Trouble Shoot File Does Not Exists!')
        close_host()
        print('- END' + self.host, 20 * '>')
# Send and execute command function
    def exce(self, command):
        connect_host(self.host, self.user, self.passwd)
        #print('- sending command', 20*'>')
        stdin, stdout, stderr = client.exec_command(command)
        for line in stdout:
            print(line.strip('\n'))

# Render configuration from a jinja2 template
class render_conf():
    def __init__(self, tempFile, paraSheet):
        self.tempFile = tempFile
        self.paraSheet = paraSheet
# Render j2 template from the xlsx's sheet
    def render(self):
        paraFile = 'pmtk_conf.xlsx'
        # outFile = 'conf_' + self.paraSheet + '_' + time.strftime('%H-%M-%d-%m-%Y', time.localtime(time.time())) + '.rsc'
        outFile = 'conf_' + self.paraSheet + '.rsc'
# Read parameters into a dict
        if os.path.exists(paraFile):
            df = pd.read_excel(paraFile, sheet_name=self.paraSheet)
            df.dropna(inplace=True)
            conf = df.set_index('Variable').to_dict()['Configuration']
        else:
            print('- ERROR: Parameter File', paraFile, ' Does Not Exists!')
# Find the temp file and use the dict to render it
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(self.tempFile)
        output = template.render(conf=conf)  #j2 temp var name = dict name
        print('- Render Result', 20 * '>')
        print(output)
# Output file
        if os.path.exists(outFile):
            os.remove(outFile)
            with open(outFile, "w+") as f:
               f.write(output)
        else:
            with open(outFile, "w+") as f:
               f.write(output)
        print('- Configuration File "' + outFile + '" Generated Successfully!')

# Send file to the mikrotik by sftp and import it
class put_conf:
    def __init__(self, host, user, passwd, filename):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.filename = filename
#
    def send_conf(self):
        localFile = r'%s' %self.filename    # Raw string
        remoteFile = '/' + self.filename    # / = root path
        command = 'import ' + self.filename
# Establish transfer connection
        trans = paramiko.Transport((self.host, 22))
        trans.connect(username=self.user, password=self.passwd)
        sftp = paramiko.SFTPClient.from_transport(trans)
        print('- sending file', 20 * '>')
        sftp.put(localFile, remoteFile)
        print('- send successful!')
        trans.close()
        print('- import configuration', 20 * '>')
        connect_host(self.host,self.user,self.passwd)
        stdin, stdout, stderr = client.exec_command(command)
        for line in stdout:
            print(line.strip('\n'))
        close_host()

# Export current configuration and pull it to local
class backup_conf:
    def __init__(self, host, user, passwd, filename):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.filename = filename
# Pull file to local from mikrotik
    def pull_file(self):
        loFile = self.filename
        reFile = '/' + self.filename
        trans = paramiko.Transport((self.host, 22))
        trans.connect(username=self.user, password=self.passwd)
        sftp = paramiko.SFTPClient.from_transport(trans)
        print('- Copying File', 20 * '>')
        sftp.get(reFile, loFile)
        print('- Done!')
        trans.close()
# Send export file command
    def export_file(self):
        command = 'export file=' + self.filename
        connect_host(self.host,self.user,self.passwd)
        client.exec_command(command)
        print('- Generating Backup File, it needs 1 mins', 20*'>')
        time.sleep(60)
        close_host()