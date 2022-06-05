import paramiko
import getpass
from time import sleep

ssh_client = paramiko.SSHClient()

# Set device kwargs
user_pswd = getpass.getpass('Enter Password: ')
router_1 = {'hostname': '169.254.38.10', 'port': '22', 'username': 'root', 'password': user_pswd}

# Delay parameters
short = 2
medium = 5
long = 20

# Connect to device
print(f"Connecting to {router_1['hostname']}")
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(**router_1, look_for_keys=False, allow_agent=False)

# Invoke Shell and send commands
shell = ssh_client.invoke_shell()
shell.send('cli\n')
sleep(medium)
shell.send('set cli screen-length 0\n')
sleep(short)
shell.send('show configuration\n')
sleep(short)

shell.send('edit private\n')
sleep(short)
shell.send('delete interfaces ge-0/0/3\n')
sleep(short)
shell.send('set interfaces ge-0/0/3 unit 0 family inet address 10.0.0.5/24\n')
sleep(short)
shell.send('show | compare\n')
sleep(medium)
shell.send('commit and-quit\n')
sleep(long)

# Decode output
output = shell.recv(10000)
output = output.decode('utf-8')
print(output)

# Close connection
if ssh_client.get_transport().is_active() == True:
    print(f"Closing connection to {router_1['hostname']}")
    ssh_client.close()

