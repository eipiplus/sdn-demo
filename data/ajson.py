from random import randint
from time import sleep
import thread as t
tmp={'THUI2':0.0,'I2CST':0.0,'CSTTHU':0.0}
tsdat={'THUI2':0.0,'I2CST':0.0,'CSTTHU':0.0}
data={}
bigsz=2**5
def testData(key):
    tsdat[key]= (tsdat[key]+randint(0,10))%2**7
    return tsdat[key]

def rsdata(key,dat):
    global tmp,bigsz
    rs = tmp[key] > dat%bigsz and dat%bigsz + bigsz - tmp[key] or dat%bigsz - tmp[key]
    tmp[key] = dat%bigsz
    return rs

def testpro():
    global testData
    for i in xrange(20):
        a = testData('THUI2')
        print a,rsdata('THUI2',a),tmp['THUI2']

def setData():
    global data
    while True:
            sleep(2)
            data["THUI2"].pop(0)
            data["THUI2"].append(rsdata('THUI2',testData('THUI2')))
            data["I2CST"].pop(0)
            data["I2CST"].append(rsdata('I2CST',testData('I2CST')))
            data["CSTTHU"].pop(0)
            data["CSTTHU"].append(rsdata('CSTTHU',testData('CSTTHU')))

def run_once(f):
    def wrapper(*args,**kwargs):
        print 'run_once wrapper'
        if not wrapper.has_run:
            wrapper.has_run=True
            return f(*args,**kwargs)
        else:
            print 'has run'
    wrapper.has_run=False
    return wrapper
@run_once
def my_function():
    data["THUI2"]=[ randint(0,20)for  i in range(10) ]
    data["I2CST"]=[ randint(0,20)for i in range(10) ]
    data["CSTTHU"]=[ randint(0,20)for  i in range(10) ]
    try:
            t.start_new_thread(setData,())
    except:
            print "Error"

#testpro()
my_function()
