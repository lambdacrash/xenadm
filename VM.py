import socket 

class VM:
    """ A simple class representing a VM"""
    id 		= "0000000"
    ip 		= ""
    name 	= "x.x.x.x"
    status	= "x.x.x.x"
    snapshots = []

    def __init__(self, ip="", name="vmname", status="status", id="0000000"):
        self.id = id
        self.ip = ip
        self.name = name
        self.status = status
        self.snapshots = []
        try: 
            self.ip = socket.gethostbyname(self.name)
        except:
            pass

