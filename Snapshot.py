class Snapshot:
    """ A simple class representing a snapshot"""
    id 		= ""
    name 	= ""
    descr   = ""
    time    = ""

    def __init__(self, name="vmname", descr="", id="0000000", time=""):
        self.id = id
        self.name = name
        self.descr = descr
        self.time = time



