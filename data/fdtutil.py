import httplib
import json
PortInfo="/wm/core/switch/all/port/json" 
FlowAccessor="/wm/staticflowentrypusher/json"
FlowClear="/wm/staticflowentrypusher/clear/all/json"
class FdtCon(object):
 
    def __init__(self, server):
        self.server = server

    def getfw(self):
        ret = self.rest_call(FlowAccessor,{}, 'GET')
        return json.loads(ret[2])
 
    def setfw(self, data):
        ret = self.rest_call(FlowAccessor,data, 'POST')
        return ret[0] == 200
 
    def rmfw(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200
    def rmallfw(self):
        ret = self.rest_call({},'GET')
        return ret[0] == 200
 
    def rest_call(self, path,data, action):
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        conn.close()
        return ret

    def portRxTx(self,dpid,port):
        res = self.rest_call(PortInfo,{},'GET')
        if res[0] != 200:
            return (-1,-1)
        res = json.loads(res[2])
        data = res[dpid]
        for e in data:
            if e['portNumber']==port:
                return (e['receiveBytes'],e['transmitBytes'])


if __name__=="__main__":
        from routeconf import flowMod
        f1=FdtCon('127.0.0.1')
        dpid='00:00:00:00:00:00:00:01'
        print f1.portRxTx(dpid,1)
        #fw=flowMod('ab2',dpid,'10.0.2.1','10.0.3.1',2,'00:01:02:03:04:05','UDP',234)
        fw=flowMod('ab2',dpid,'10.0.2.1','10.0.3.1',24,'00:01:02:03:04:05','UDP',24)
        fw['actions']='output=3'
        print fw
        print f1.setfw(fw)

