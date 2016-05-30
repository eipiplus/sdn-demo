from fdtutil import FdtCon

srcip='srcip'
dstip='dstip'

fport=4
tport=2

srcmac='srcmac'
dstmac='dstmac'

thu='thu-controller'
i2='i2-controller'
cst='cst-controller'

ctrl=[thu,cst,cst,i2]

swthu='thu-0'
swcst1='cst-1'
swcst2='cst-2'
swi2='i2-3'
sw=[swthu,swcst1,swcst2,swi2]
dcpt={}
dcpt[(0,1)]=1
dcpt[(1,0)]=10
dcpt[(1,2)]=12
dcpt[(2,1)]=21
dcpt[(2,3)]=23
dcpt[(3,2)]=32
dcpt[(3,0)]=30
dcpt[(0,3)]=3

nmlist=[]
cnt=0

def flowMod(name,dpid,srcip,dstip,inport,srcmac='',protocol='',dstport=0,priority=1):
    """Set flow form name dpid, srcip,dstip,inport. optimal for srcmac,protocol,dstport,priority"""
    res={}
    res['name']=name
    res['ether-type']='0x800'
    res['switch']=dpid
    res['ingress-port']=str(inport)
    res['src-ip']=srcip
    res['dst-ip']=dstip
    res['priority']=str(priority)
    if srcmac != '':
        res['src-mac']=srcmac
    if protocol != '':
        res['protocol'] = protocol == 'TCP' and '6' or '17'
    if dstport != 0:
        res['dst-port']=str(dstport)
    return res


def droppkt(dpid,port,prior):
    global cnt,nmlist
    fw={}
    name='flow-'+str(cnt)
    nmlist += [(name,dpid)]
    cnt += 1
    fw['name']=name
    fw['ingress-port']=port
    fw['priority']=prior
    return fw

def rmallflow():
    for e in ctrl:
        fdtu=FdtCon(e)
        fdtu.rmallfw()

def normal():
    #rmallflow()
    path=[0,3]
    port=(fport,tport)
    fws=pathfw(path,(srcip,dstip),(srcmac,dstmac),port)
    for x,fw in enumerate(fws):
        fdt=FdtCon(ctrl[ path[x]  ])
     #   fdt.setfw(fw)
        print fdt.server,fw
def linkdown():
    #rmallflow()
    path=[0,1,2,3]
    port=(fport,tport)
    fws=pathfw(path,(srcip,dstip),(srcmac,dstmac),port)
    ## add drop function
    for x,fw in enumerate(fws):
        fdt=FdtCon(ctrl[ path[x]  ])
     #   fdt.setfw(fw)
        print fdt.server,fw



def pathfw(path,ip,mac,port,opt=('',0,1)):
        global cnt,nmlist
        if len(path)<2:
                return []
        srcip,dstip=ip
        srcmac,dstmac=mac
        begport,endport=port
        protocol,dstport,prior=opt
        ret = []
        name = 'flow-'+str(cnt)
        fw=flowMod(name,sw[path[0]],srcip,dstip,begport,srcmac,protocol,dstport,prior)
        fw['actions']='output=%d'%(dcpt[(path[0],path[1])])
        ret += [fw]
        nmlist += [(name,sw[path[0]])]
        cnt += 1
        for x,e in enumerate(path[:-2]):
                eb = path[x+1]
                ec = path[x+2]
                inport=dcpt[(eb,e)]
                name = 'flow-'+str(cnt)
                cnt += 1
                nmlist += [(name,sw[eb])]
                fw=flowMod(name,sw[eb],srcip,dstip,inport,srcmac,protocol,dstport,prior)
                fw['action']='output=%d'%(dcpt[(eb,ec)])
                ret += [fw]
        name = 'flow-'+str(cnt)
        fw=flowMod(name,sw[path[-1]],srcip,dstip,dcpt[(path[-1],path[-2])],srcmac,protocol,dstport,prior)
        fw['actions']='set-dst-mac=%s,output=%d'%(dstmac,endport)
        ret += [fw]
        nmlist += [(name,sw[path[-1]])]
        cnt += 1
        return ret

if __name__=='__main__':
    linkdown()
    normal()
