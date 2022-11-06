import paramiko
import os
host = os.getenv('SSHIP')

try:
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=22, username="redhat", password="redhat")
    print("login Success !!")
    stdin, stdout, stderr = client.exec_command('oc get deploy -n busybox --insecure-skip-tls-verify=true --no-headers  | awk \'{print $1}\' ')
    result = stdout.readlines()
    print(result)
    print(stderr.readlines())
except Exception as e:
    print(e)
finally:
    client.close()