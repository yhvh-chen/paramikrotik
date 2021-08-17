# paramikrotik

1	Introduction

Project Paramirotik uses to automatically send pre-defined troubleshooting commands, generate RouterOS configuration from the template, send a configuration file, backup configuration with single or multiple MikroTik clients.

2	Project Overview

2.1	Development environment 

•	Language: Python 3.9.5

•	Modules:  paramiko - 2.7.2, pandas  - 1.3.2, jinja 2 - 3.0.1, os, time

•	IDE: Pycharm2021.2(Community Edition)

•	Notes: SSH connection needs to be configured between host and client, currently only support password authentication.


2.2	Code Structure

![paramikrotik](https://user-images.githubusercontent.com/73627640/129671648-708205b8-a92e-4d1f-b3f6-d9c6938aa834.png)


2.3	Files Structure

Paramikrotik has five files, description can be found below. All files must be put in the same path.

1.	paramikrotik.py: project mian file

3.	pmtk.ipynb: jupyter running file

5.	pmtk_comm.xlsx: commands file

7.	pmtk_conf.xlsx: configuration parameters file

9.	xxx.j2:  configuration template file


3	Modules and classes

3.1	Modules

•	Paramiko: Establishing ssh and sftp connection, sending command, sending and pulling files from MikroTik router.

•	Pandas: Reading excel files.

•	Jinja2: Render configuration file from j2 template.

•	OS: File I/O.

•	Time: Command timing controlling.


3.2	Classes

3.2.1	Send_commd 

Function: Batch sends commands from xlsx file. Engineers can define the commands in the excel sheet, and specific sheet’s name to send different commands.

	send_commd(host, user, passwd, commSheet)

•	host: ip address of Mikrotik client

•	user: ssh username of Mikrotik client

•	passwd: ssh password of Mikrotik client

•	commSheet: sheet name in file pmtk_comm.xlsx


	tb_shoot

Send TS command in tsFile's sheet

	exec

Send and execute the command on Mikrotik

3.2.2	render_conf

Function: Generate configuration from a template file and excel files’ sheet. It uses jinja2 as the template file and parameters store in the pmtk_conf.xlsx. Engineers can customize their template file, can define the parameters into excel’s sheet.

	Render_conf(tempFile, paraSheet)

•	tempFile: file name of jinja2 template

•	paraSheet: sheet name in file pmtk_conf.xlsx

	render

Render configuration from a jinja2 template

3.2.3	put_conf 

Function: Send the configuration to a Mikrotik client, and import it.

	put_conf(host, user, passwd, filename)

•	host: ip address of Mikrotik client

•	user: ssh username of Mikrotik client

•	passwd: ssh password of Mikrotik client

•	filename: filename of the configuration

	send_conf

send a configuration file to the Mikrotik client and import it

3.2.4	backup_conf 

Function: Export current configuration to file on Mikrotik client. Pull a file from a Mikrotik client to the local host.

	pull_conf(host, user, passwd, filename)

•	host: ip address of Mikrotik client

•	user: ssh username of Mikrotik client

•	passwd: ssh password of Mikrotik client

•	filename: filename of the configuration

	pull_file

Pull file to local from Mikrotik

	export_file

export current configuration as a file on Mikrotik

4	Configuration template

4.1	Customize template

Paramikrotik use jinja2 to generate configuration, more details can be found on(https://jinja.palletsprojects.com/en/3.0.x/).

All variables begin with ‘conf.’, and variables are capital letters, for example: {{  conf. LAN_ADD }}

	RouterOS configuration:

add address=192.168.88.1/24 comment=LAN_Address interface=bridge \

network=192.168.88.0

	J2 template:

add address={{ conf.LAN_ADD }} comment=LAN_Address interface=bridge \

network={{ conf.LAN_NET }}

	pmtk_conf.xlsx:

Variable	Configuration

LAN_ADD	192.168.88.1/24

LAN_NET	192.168.88.0


5	Run and test

5.1	Recommend

Recommend run Paramiktotik on Jupyter, also can run it on IDE or CMD. It gives a running example on the jupyter file.

