from flask import Flask, flash, redirect
from flask import render_template
from VM import VM 
from Server import Server
import socket

def list_vms():
    vms = []
    svms = server.list_vm()
    for vm in svms:
        vms.append(vm)
    # ret = xe list blablabla
    # parse ret
    #vms.append(VM(ip="10.1.86.244", name="VM Toto", status="Starting"))
    #vms.append(VM(ip="10.1.86.24", name="VM Tata", status="Stop"))
    return vms 

server = Server(id="1", ip="10.1.86.8", user="root", password="secret")

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/start/<vmid>')
def start_vm(vmid):
    # do some shit xe blablabla
    ret = server.start_vm(vmid)
    flash(ret)	
    return redirect("/")

@app.route('/stop/<vmid>')
def stop_vm(vmid):
    # do some shit xe blablabla
    ret = server.stop_vm(vmid)
    flash(ret)	
    return redirect("/")

@app.route('/snap/<vmid>')
def snap_vm(vmid):
    # do some shit xe blablabla
    flash("VM "+vmid+" about to be snapshoted")	
    return redirect("/")

@app.route('/')
def index():
    return render_template("index.html", servername=socket.gethostname(), vms=list_vms())

if __name__ == '__main__':
    app.debug = True 
    app.run(host='0.0.0.0')
