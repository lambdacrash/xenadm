import paramiko
from VM import VM

class Server:
    id = ""
    ip = ""
    user = "root"
    password = "secret"
    vms = []

    def __init__(self, id="0", ip="0", vms=[], user="root", password="secret"):
        self.id = id
        self.ip = ip
        self.vms = vms
        self.user = user
        self.password = password

    def start_vm(self, id=-1):
        if id < 0:
            return
        for vm in self.vms:
            if vm.id == id:
                if vm.status!="halted":
                    return "Unable to start a running VM"
                ssh = paramiko.SSHClient()
                ssh.load_system_host_keys()
                ssh.connect(self.ip, username=self.user, password=self.password)
                stdin, stdout, stderr = ssh.exec_command('xe vm-start uuid="'+vm.id+'"')
                ret = stdout.read()
                ssh.close()
                return ret



    def stop_vm(self, id=-1):
        if id < 0:
            return
        for vm in self.vms:
            if vm.id == id:
                if vm.status!="running":
                    return "Unable to stop an halted VM"
                ssh = paramiko.SSHClient()
                ssh.load_system_host_keys()
                ssh.connect(self.ip, username=self.user, password=self.password)
                stdin, stdout, stderr = ssh.exec_command('xe vm-shutdown uuid="'+vm.id+'"')
                ret = stdout.read()
                ssh.close()
                return ret
    #    for vm in self.vms:
    #        if vm.id == id:

    def snap_vm(self, id=-1):
        if id < 0:
            return
    #    for vm in self.vms:
    #        if vm.id == id:

    def list_vm(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(self.ip, username=self.user, password=self.password)
        stdin, stdout, stderr = ssh.exec_command('xe vm-list tags="xenadm"')
        ret = stdout.read()
        ssh.close()
        self.vms = []
        name = ""
        id=""
        status=""
        for l in ret.split("\n"):
            if "uuid" in l:
                id = l.split(" : ")[-1]
            elif "name-label" in l:
                name = l.split(": ")[-1]
            elif "power-state" in l:
                status = l.split(": ")[-1]
                self.vms.append(VM(id=id, name=name, status=status))
        return self.vms
