import paramiko
import re


def auth_data(ip):
    if ip == '127.0.0.1':
        return 'login', 'password'


def get_connection_client(host='127.0.0.1', connection_type='ssh'):

    if connection_type == 'ssh':
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        user, psw = auth_data(host)

        ssh_client.connect(hostname=host_address, username=user, password=psw)

        transport = ssh_client.get_transport()
        sftp_client = transport.open_sftp_client()

        return sftp_client
    else:
        print('This connection is not supported: %s' % connection_type)
        return None


def get_logs(log_name, client, ID):
    """
    This function looks for log_name file,
    opens it, finds line with ID and prints
    this line and +-lines
    :param log_name: log file name
    :param client: server with logs directory
    :param ID: line id to look for
    :return: none
    """
    for name in client.listdir(path='/var/log/'):
        if re.match('%s*.*.log' % log_name, name):
            log_name = name
            break

    line_num = 0
    lines = list()
    with client.open('/var/log/%s' % log_name) as log_file:
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


file_name = input('Enter name of log file: ')
host_address = input('Enter IP address: ')
ID = input('Enter ID for search: ')

get_logs(file_name, get_connection_client(host=host_address), ID)
