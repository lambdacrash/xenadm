from flask import Flask, flash, redirect
from flask import render_template
from VM import VM 
import socket

def list_vms():
    vms = []
    # ret = xe list blablabla
    # parse ret
    vms.append(VM(ip="10.1.86.244", name="VM Toto", status="Starting"))
    vms.append(VM(ip="10.1.86.24", name="VM Tata", status="Stop"))
    return vms 


app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/start/<vmid>')
def start_vm(vmid):
    # do some shit xe blablabla
    flash("VM "+vmid+" about to be started")	
    return redirect("/")

@app.route('/stop/<vmid>')
def stop_vm(vmid):
    # do some shit xe blablabla
    flash("VM "+vmid+" about to be stopped")	
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
