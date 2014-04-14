from flask import Flask, flash, redirect, request
from flask import render_template
from Server import Server
from VM import VM 
import ConfigParser
import random
import socket
import sys


server = None
app = Flask(__name__)

def ConfigSectionMap(section, config_file):
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def list_vms():
    vms = []
    svms = server.list_vm()
    for vm in svms:
        server.list_snapshots(vm)
        vms.append(vm)
    return vms 


@app.route('/start/<vmid>')
def start_vm(vmid):
    flash("VM "+vmid+" about to be started")	
    ret = server.start_vm(vmid)
    if ret != "":
        flash(ret)	
    return redirect("/")

@app.route('/stop/<vmid>')
def stop_vm(vmid):
    flash("VM "+vmid+" about to be halted")	
    ret = server.stop_vm(vmid)
    if ret != "":
        flash(ret)	
    return redirect("/")

@app.route('/snap/<vmid>', methods=['POST'])
def snap_vm(vmid):
    flash("Snapshot of "+vmid+" created with name "+request.form["snapshot_name"])	
    ret = server.snap_vm(vmid, name=request.form["snapshot_name"], descr=request.form["snapshot_description"])
    if ret != "":
        flash(ret)	
    return redirect("/")

@app.route('/snap/<vmid>', methods=['GET'])
def snap_vm_form(vmid):
    vm = server.get_vm(vmid)
    return render_template("snapshot_form.html", servername=socket.gethostname(), vm=vm)

@app.route('/revert/<vmid>/<sid>', methods=['GET'])
def snap_revert(vmid, sid):
    flash("VM "+vmid+" was reverted with the snapshot "+str(sid))	
    vm = server.get_vm(vmid)
    ret = server.revert_snapshot(vmid, sid)
    if ret != "":
        flash(ret)	
    return render_template("index.html", servername=socket.gethostname(), vm=vm)

@app.route('/viewsnap/<vmid>')
def view_snap(vmid):
    vm = server.get_vm(vmid)
    return render_template("snapshots.html", servername=socket.gethostname(), vm=vm)

@app.route('/')
def index():
    return render_template("index.html", servername=socket.gethostname(), vms=list_vms())

if __name__ == '__main__':
    configFile = "./server.conf"
    if len(sys.argv) > 1:
        configFile = sys.argv[1]
        print("Use "+configFile+" from command line parameter for master server configuration")
    else :
        print("Use "+configFile+" as default for master server configuration")

    app.secret_key = str(('%09x' % random.randrange(16**9)))
    listen = ConfigSectionMap("Configuration", configFile)['listen']    
    port = ConfigSectionMap("Configuration", configFile)['port']    
    ms = ConfigSectionMap("MasterServer", configFile)
    server = Server(id=str(ms["id"]), ip=str(ms["ip"]), user=str(ms["user"]), password=str(ms["password"]))
    app.debug = True 
    app.run(host=str(listen), port=int(port))
