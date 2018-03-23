import paramiko
import re


def auth_data(ip):
    if ip == '172.26.149.118':
        return 'svc_nwvtb', '1qaz@WSX'


file_name = input('Enter name of log file: ')
host_address = input('Enter IP address: ')
ID = input('Enter ID for search: ')

line_num = 0
lines = list()

if not host_address:
    host_address = '172.26.149.118'

ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

user, psw = auth_data(host_address)

ssh_client.connect(hostname=host_address, username=user, password=psw)

transport = ssh_client.get_transport()
sftp_client = transport.open_sftp_client()
for name in sftp_client.listdir(path='/var/log/'):
    if re.match('%s*.*.log' % file_name, name):
        file_name = name
        break

with sftp_client.open('/var/log/%s' % file_name) as log_file:
    for num, line in enumerate(log_file):
        lines.append((num, line))
        if len(lines) > 100:
            del lines[:1]
        if ID in line and not line_num:
            print(num, line)
            line_num = num
        if line_num and (line_num + 100 == num):
            break
    for num, line in lines:
        print(num, line.strip())
