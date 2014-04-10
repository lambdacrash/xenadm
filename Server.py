import paramiko
from VM import VM
from Snapshot import Snapshot

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

    def revert_snapshot(self, vmid, sid):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(self.ip, username=self.user, password=self.password)
        vm = self.get_vm(vmid)
        stdin, stdout, stderr = ssh.exec_command('xe snapshot-revert uuid="'+vmid+'" snapshot-uuid="'+sid+'"')
        ret = stdout.read()
        ssh.close()
        return ret

    def snap_vm(self, id=-1, name="", descr=""):
        if id < 0 or name=="":
            return
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(self.ip, username=self.user, password=self.password)
        vm = self.get_vm(id)
        stdin, stdout, stderr = ssh.exec_command('xe vm-snapshot uuid="'+id+'" new-name-label="'+str(len(vm.snapshots))+'-'+name+'" new-name-description="'+descr+'"')
        ret = stdout.read()
        ssh.close()
        return ret

    def get_vm(self, id=-1):
        if id < 0:
            return
        for vm in self.vms:
            if vm.id == id:
                return vm
        return []

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

    def list_snapshots(self, vm):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(self.ip, username=self.user, password=self.password)
        stdin, stdout, stderr = ssh.exec_command('xe snapshot-list snapshot-of='+vm.id+' params=all')
        ret = stdout.read()
        ssh.close()
        vm.snapshots = []
        name = ""
        id=""
        descr=""
        time=""
        for l in ret.split("\n"):
            if "uuid ( RO)" in l:
                id = l.split(" : ")[-1]
            elif "snapshot-time" in l:
                time = l.split(": ")[-1]
            elif "name-label" in l:
                name = l.split(": ")[-1]
            elif "name-description" in l:
                descr = l.split(": ")[-1]
                vm.snapshots.append(Snapshot(id=id, name=name, descr=descr, time=time))
        vm.snapshots.sort(key = lambda x : x.name)
        return vm.snapshots

