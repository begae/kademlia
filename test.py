class Test:
    def __init__(self, addr, port, nid):
        self.addr = addr
        self.port = port
        self.nid = nid
        self.info = {'addr':addr, 'port':port, 'nid':nid}

test = Test(1,2,3)
print(test.info)