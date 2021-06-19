import b0RemoteApi
import time

with b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient','b0RemoteApi',60) as client:    

    def callb(msg):
        print(msg)
   
    client.simxAddStatusbarMessage('Hello',client.simxDefaultPublisher())
    s1=client.simxGetObjectHandle('shape1',client.simxServiceCall())
    s2=client.simxGetObjectHandle('shape2',client.simxServiceCall())
    prox=client.simxGetObjectHandle('prox',client.simxServiceCall())
    vis=client.simxGetObjectHandle('vis',client.simxServiceCall())
    fs=client.simxGetObjectHandle('fs',client.simxServiceCall())
    coll=client.simxGetCollisionHandle('coll',client.simxServiceCall())
    dist=client.simxGetDistanceHandle('dist',client.simxServiceCall())
    
    '''
    res=client.simxAuxiliaryConsoleOpen('theTitle',50,4,[10,400],[1024,100],[1,1,0],[0,0,0],client.simxServiceCall())
    client.simxAuxiliaryConsolePrint(res[1],'Hello World!!!\n',client.simxServiceCall())
    time.sleep(1)
    client.simxAuxiliaryConsoleShow(res[1],False,client.simxServiceCall())
    time.sleep(1)
    client.simxAuxiliaryConsoleShow(res[1],True,client.simxServiceCall())
    time.sleep(1)
    client.simxAuxiliaryConsoleClose(res[1],client.simxServiceCall())
    client.simxStartSimulation(client.simxServiceCall())
    client.simxStopSimulation(client.simxServiceCall())
    '''
    '''
    res=client.simxAddDrawingObject_points(8,[255,0,255],[0,0,0,1,0,0,0,0,1],client.simxServiceCall())
    time.sleep(1)
    client.simxRemoveDrawingObject(res[1],client.simxServiceCall())
    res=client.simxAddDrawingObject_spheres(0.05,[255,0,0],[0,0,0,1,0,0,0,0,1],client.simxServiceCall())
    time.sleep(1)
    client.simxRemoveDrawingObject(res[1],client.simxServiceCall())
    res=client.simxAddDrawingObject_cubes(0.05,[255,0,0],[0,0,0,1,0,0,0,0,1],client.simxServiceCall())
    time.sleep(1)
    client.simxRemoveDrawingObject(res[1],client.simxServiceCall())
    res=client.simxAddDrawingObject_segments(4,[0,255,0],[0,0,0,1,0,0, 1,0,0,0,0,1, 0,0,1,0,0,0],client.simxServiceCall())
    time.sleep(1)
    client.simxRemoveDrawingObject(res[1],client.simxServiceCall())
    res=client.simxAddDrawingObject_triangles([255,128,0],[0,0,0, 1,0,0, 0,0,1],client.simxServiceCall())
    time.sleep(1)
    client.simxRemoveDrawingObject(res[1],client.simxServiceCall())
    '''
    '''
    #res=client.simxCallScriptFunction('myFunction@DefaultCamera','sim.scripttype_customizationscript',"Hello World :)",[255,0,255],None,None,client.simxServiceCall())
    print(client.simxCheckCollision(s1[1],s2[1],client.simxServiceCall()))
    print(client.simxCheckDistance(s1[1],s2[1],0,client.simxServiceCall()))
    print(client.simxCheckProximitySensor(prox[1],s2[1],client.simxServiceCall()))
    print(client.simxCheckVisionSensor(vis[1],s2[1],client.simxServiceCall()))
    print(client.simxReadCollision(coll[1],client.simxServiceCall()))
    print(client.simxReadDistance(dist[1],client.simxServiceCall()))
    print(client.simxReadProximitySensor(prox[1],client.simxServiceCall()))
    print(client.simxReadVisionSensor(vis[1],client.simxServiceCall()))
    print(client.simxReadForceSensor(fs[1],client.simxServiceCall()))
    print(client.simxBreakForceSensor(fs[1],client.simxServiceCall()))
    client.simxSetFloatSignal('floatSignal',123.456,client.simxServiceCall())
    client.simxSetIntegerSignal('integerSignal',59,client.simxServiceCall())
    client.simxSetStringSignal('stringSignal','Hello World',client.simxServiceCall())
    print(client.simxGetFloatSignal('floatSignal',client.simxServiceCall()))
    print(client.simxGetIntegerSignal('integerSignal',client.simxServiceCall()))
    print(client.simxGetStringSignal('stringSignal',client.simxServiceCall()))
    time.sleep(1)
    client.simxClearFloatSignal('floatSignal',client.simxServiceCall())
    client.simxClearIntegerSignal('integerSignal',client.simxServiceCall())
    client.simxClearStringSignal('stringSignal',client.simxServiceCall())
    time.sleep(1)
    print(client.simxGetFloatSignal('floatSignal',client.simxServiceCall()))
    print(client.simxGetIntegerSignal('integerSignal',client.simxServiceCall()))
    print(client.simxGetStringSignal('stringSignal',client.simxServiceCall()))

    client.simxCheckProximitySensor(prox[1],s2[1],client.simxDefaultSubscriber(callb))
    startTime=time.time()
    while time.time()<startTime+5: 
        client.simxSpinOnce()
    '''
    '''
    print(client.simxSetObjectPosition(s1[1],-1,[0,0,0.2],client.simxServiceCall()))
    time.sleep(1)
    print(client.simxSetObjectOrientation(s1[1],-1,[0,0,0.2],client.simxServiceCall()))
    print(client.simxGetObjectOrientation(s1[1],-1,client.simxServiceCall()))
    time.sleep(1)
    print(client.simxSetObjectQuaternion(s1[1],-1,[0,0,0.2,1],client.simxServiceCall()))
    print(client.simxGetObjectQuaternion(s1[1],-1,client.simxServiceCall()))
    time.sleep(1)
    print(client.simxSetObjectPose(s1[1],-1,[0.1,0.1,0,0,0,0,1],client.simxServiceCall()))
    print(client.simxGetObjectPose(s1[1],-1,client.simxServiceCall()))
    time.sleep(1)
    matr=client.simxGetObjectMatrix(s1[1],-1,client.simxServiceCall())
    print(matr)
    matr[1][3]=0
    matr[1][7]=0
    print(client.simxSetObjectMatrix(s1[1],-1,matr[1],client.simxServiceCall()))
'''    
    '''
    print(client.simxCallScriptFunction('myFunction@DefaultCamera','sim.scripttype_customizationscript',["Hello World :)",[255,0,255],None,None],client.simxServiceCall()))
    print(client.simxCallScriptFunction('myFunction@DefaultCamera','sim.scripttype_customizationscript','Hello World :)',client.simxServiceCall()))
    print(client.simxCallScriptFunction('myFunction@DefaultCamera','sim.scripttype_customizationscript',59,client.simxServiceCall()))
    print(client.simxCallScriptFunction('myFunction@DefaultCamera','sim.scripttype_customizationscript',None,client.simxServiceCall()))
    '''
    time.sleep(1)
    copies=client.simxCopyPasteObjects([s1[1],s2[1]],0,client.simxServiceCall())
    print(copies)
    time.sleep(1)
    client.simxRemoveObjects(copies[1],0,client.simxServiceCall())
    client.simxCloseScene(client.simxServiceCall())