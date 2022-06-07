import paramiko
import util
from util import wait as sleep

ssh_client = paramiko.SSHClient()

# Set device kwargs
srjp = util.getcreds('srjp')
cicd_vm = util.getcreds('cicdvm')

# Connect to device
print(f"Connecting to {srjp['hostname']}...")
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(**srjp, look_for_keys=False, allow_agent=False)

shell = ssh_client.invoke_shell()
shell.send(f"ssh {cicd_vm['hostname']}\n")
sleep()
shell.send(f"{cicd_vm['password']}\n")
sleep()
shell.send('docker ps\n')
sleep()

# Decode output
output = shell.recv(10000)
output = output.decode('utf-8')
print(output)

# Close connection
if ssh_client.get_transport().is_active() == True:
    print(f"Closing connection to {srjp['hostname']}...")
    ssh_client.close()