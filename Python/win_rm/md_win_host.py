'''
Author       : Kui.Chen
Date         : 2023-03-13 11:46:20
LastEditors  : Kui.Chen
LastEditTime : 2023-03-13 14:45:10
FilePath     : \Scripts\Python\win_rm\md_win_host.py
Description  : 循环修改Windows host名单
Copyright    : Copyright (c) 2023 by Kui.Chen, All Rights Reserved.
'''

import winrm

def remote_server(remote_host, command): 
    remote_username = 'tableau'
    remote_password = 'wixj-2342'
    session         = winrm.Session('http://'+remote_host+':5985/wsman', 
                            auth                   = (remote_username, remote_password),
                            transport              = 'ntlm',
                            server_cert_validation = 'ignore')
    # ^ --- Run commands ---
    # result = session.run_cmd(command) 
    # ^ --- Run Powershell ---
    result = session.run_ps(command) 
    print (result.std_out.decode("utf-8"))
    # return result.std_out.decode()

nodes = [
## IP Address 		    HostName	        Role
# "10.122.36.100",	#	"SYPQLIKSENSE15"	[PRD] Proxy Engine 04"
# "10.122.36.106",	#	"SYPQLIKSENSE18"	[PRD] Proxy Engine 05"
# "10.122.36.107",	#	"SYPQLIKSENSE11"	[PRD] Proxy Engine 01"
# "10.122.36.108",	#	"SYPQLIKSENSE12"	[PRD] Proxy Engine 02"
# "10.122.36.109",	#	"SYPQLIKSENSE13"	[PRD] Proxy Engine 03"
# "10.122.36.110",	#	"SYPQLIKSENSE14"	[PRD] API 02"
# "10.122.36.119",	#	"SYPQLIKSENSE03"	[PRD] API 01"
# "10.122.36.120",	#	"SYPQLIKSENSE04"	[PRD] Central Master & Scheduler Master"
"10.122.36.121",	#	"SYPQLIKSENSE05"	[PRD] Scheduler 05"
"10.122.36.122",	#	"SYPQLIKSENSE06"	[PRD] Central Candidate & Scheduler 01"
"10.122.36.123",	#	"SYPQLIKSENSE07"	[PRD] Scheduler 02"
"10.122.36.124",	#	"SYPQLIKSENSE08"	[PRD] Scheduler 03"
"10.122.36.220",	#	"SYPQLIKSENSE17"	[PRD] Scheduler 04"
"10.122.36.111",	#	"PEKWPQLIK05"	    [DEV] Central Master & Scheduler Master"
"10.122.36.112",	#	"PEKWPQLIK06"	    [DEV] Central Candidate & Scheduler 01"
"10.122.36.114",	#	"PEKWPQLIK01"	    [DEV] Proxy Engine 01"
"10.122.36.115",	#	"PEKWPQLIK03"	    [DEV] Proxy Engine 02"
"10.122.36.116",	#	"PEKWPQLIK04"	    [DEV] Proxy Engine 03"
"10.122.36.128" 	#	"SYPQLIKSENSE09"	[DEV] Scheduler 02"
]
ps1  = """
$hostFile = "C:\Windows\System32\drivers\etc\hosts"
# 创建备份目录到用户下载目录中
$downloadFolder = [Environment]::GetFolderPath([Environment+SpecialFolder]::Userprofile) + '\Downloads'
$backupFolder = $downloadFolder + '\Hosts_Backup_' + (Get-Date -Format "yyyyMMddTHHmmss")
New-Item -ItemType Directory -Path $backupFolder | Out-Null
# 备份 host 文件
Copy-Item $hostFile -Destination $backupFolder
Write-Host $env:COMPUTERNAME ": Successfully back up the Hosts file to " $backupFolder
# 更新 host 文件内容
$fileContent = @"
\r\n
# Add host list $(Get-Date -Format 'yyyyMMddTHHmmss') \r\n
192.168.0.1     www.example.com \r\n
192.168.0.2     www.test.com \r\n
"@

Add-Content -Path $hostFile -Value $fileContent
Write-Host $env:COMPUTERNAME ": The host file is modified."
"""

if __name__ == '__main__':
    for node in nodes:
        remote_server(node, ps1)