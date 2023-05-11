--******IMPOTRANT******
--simRemoteApi.start(19999) -- input this line in Lua command

function sysCall_init()
    corout=coroutine.create(coroutineMain)
end

function sysCall_actuation()
    if coroutine.status(corout)~='dead' then
        local ok,errorMsg=coroutine.resume(corout)
        if errorMsg then
            error(debug.traceback(corout,errorMsg),2)
        end
    end
end

setGripperData=function(open,velocity,force)
    if not velocity then
        velocity=0.10
    end
    if not force then
        force=100
    end
    if not open then
        velocity=-velocity
    end
    
    local dat={}
    dat.velocity=velocity
    dat.force=force
    sim.writeCustomDataBlock(gripperHandle,'activity',sim.packTable(dat))
end

function moveToPoseCallback(q,velocity,accel,auxData)
    sim.setObjectPose(auxData.target,-1,q)
    simIK.applyIkEnvironmentToScene(auxData.ikEnv,auxData.ikGroup)
end

function moveToPose_viaIK(maxVelocity,maxAcceleration,maxJerk,targetQ,auxData)
    local currentQ=sim.getObjectPose(auxData.target,-1)
    return sim.moveToPose(-1,currentQ,maxVelocity,maxAcceleration,maxJerk,targetQ,moveToPoseCallback,auxData,nil)
end

function moveToConfigCallback(config,velocity,accel,auxData)
    for i=1,#auxData.joints,1 do
        local jh=auxData.joints[i]
        if sim.getJointMode(jh)==sim.jointmode_force and sim.isDynamicallyEnabled(jh) then
            sim.setJointTargetPosition(jh,config[i])
        else    
            sim.setJointPosition(jh,config[i])
        end
    end
end

function moveToConfig_viaFK(maxVelocity,maxAcceleration,maxJerk,goalConfig,auxData)
    local startConfig={}
    for i=1,#auxData.joints,1 do
        startConfig[i]=sim.getJointPosition(auxData.joints[i])
    end
    sim.moveToConfig(-1,startConfig,nil,nil,maxVelocity,maxAcceleration,maxJerk,goalConfig,nil,moveToConfigCallback,auxData,nil)
end

function coroutineMain()
    -- Initialize some values:
    local simJoints={}
    for i=1,6,1 do
        simJoints[i]=sim.getObjectHandle('UR3_joint'..i)
    end
    
    local simTarget = sim.createDummy(0.01)
    sim.setObjectPosition(simTarget,-1,{0,0,0})  --initialize the simTaget
    
    local simTip=sim.getObjectHandle('tip')
    local modelBase=sim.getObjectHandle('UR3')  -- sim.handle_self
    gripperHandle=sim.getObjectHandle('RG2')
    
    ikEnv=simIK.createEnvironment()

    -- Prepare the ik group, using the convenience function 'simIK.addIkElementFromScene':
    ikGroup=simIK.createIkGroup(ikEnv)
    simIK.addIkElementFromScene(ikEnv,ikGroup,modelBase,simTip,simTarget,simIK.constraint_pose)

    -- FK movement data:
    local initConf={0,0,0,0,0,0}
    local vel=150
    local accel=75
    local jerk=120
    local maxVel={vel*math.pi/180,vel*math.pi/180,vel*math.pi/180,vel*math.pi/180,vel*math.pi/180,vel*math.pi/180}
    local maxAccel={accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180}
    local maxJerk={jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180}
    

    -- IK movement data 
    local ikMaxVel={0.3,0.3,0.3,0.3}
    local ikMaxAccel={0.05,0.05,0.05,0.05}
    local ikMaxJerk={0.05,0.05,0.05,0.05}

    --local pickConfig={-70.1*math.pi/180,18.85*math.pi/180,93.18*math.pi/180,68.02*math.pi/180,109.9*math.pi/180,90*math.pi/180}
    --local dropConfig1={-183.34*math.pi/180,14.76*math.pi/180,78.26*math.pi/180,-2.98*math.pi/180,-90.02*math.pi/180,86.63*math.pi/180}
    --local dropConfig2={-197.6*math.pi/180,14.76*math.pi/180,78.26*math.pi/180,-2.98*math.pi/180,-90.02*math.pi/180,72.38*math.pi/180}
    --local dropConfig3={-192.1*math.pi/180,3.76*math.pi/180,91.16*math.pi/180,-4.9*math.pi/180,-90.02*math.pi/180,-12.13*math.pi/180}
    --local dropConfig4={-189.38*math.pi/180,24.94*math.pi/180,64.36*math.pi/180,0.75*math.pi/180,-90.02*math.pi/180,-9.41*math.pi/180}
    
    --local dropConfigs={dropConfig1,dropConfig2,dropConfig3,dropConfig4}
    --local dropConfigIndex=1
    
    objects={'fork','airplane','heatgun','cup','powerdrill','cleanser','clamp','chain','banana','gun','11','12','13','14','15','16','17','18','19','20'}   --objects' name ,'Cuboid6','Cuboid4',
    sim.setIntegerSignal('objectNumber',#objects)
    local droppedPartsCnt=0

    setGripperData(true)  -- open the gripper
    --sim.setInt32Param(sim.intparam_current_page,0)  -- change camera's perspective 

    local data={}
    data.ikEnv=ikEnv
    data.ikGroup=ikGroup
    data.tip=simTip
    data.target=simTarget
    data.joints=simJoints
    
    destConfig2={0,0,0,0,0,0}
    destConfig={-90*math.pi/180,0,110*math.pi/180,-110*math.pi/180,0,0}
    
    while droppedPartsCnt<#objects do
        --Send request to the client to acquire the images and detect the grasps
        sim.wait(0.3)
        sim.setStringSignal('sendImages','start')
        
        --Get reply of grasp params from the client
        sim.wait(0.5)
        sendGrasps=sim.waitForSignal('sendGrasps')
        local X=sim.getFloatSignal('graspCenterX')
        local Y=sim.getFloatSignal('graspCenterY')
        local Z=sim.getFloatSignal('graspCenterZ')
        local graspCenter={X,Y,Z}--local graspCenter={0.375,0.05,0.02} cup02 0.11, cucoid6 0.02
        local graspAngle=sim.getFloatSignal('graspAngle') --graspAngle= 30*math.pi/180
        sim.clearStringSignal('sendGrasps')
        sim.clearFloatSignal('graspCenterX')
        sim.clearFloatSignal('graspCenterY')
        sim.clearFloatSignal('graspAngle')
        
        --update the grasp info
        sim.setObjectPosition(data.target,-1,graspCenter)
        sim.setObjectOrientation(data.target, data.target, {0,0,graspAngle})
        
        joint1_x=-0.065125
        joint1_y=0.13791
        sine=(Y-joint1_y)/math.sqrt((Y-joint1_y)*(Y-joint1_y)+(X-joint1_x)*(X-joint1_x)) --math.asin(sine)
        
        local pickConfig={0*math.pi/180,0*math.pi/180,85*math.pi/180,-85*math.pi/180,0*math.pi/180,-1*graspAngle} --0*math.pi/180
        
        moveToConfig_viaFK(maxVel,maxAccel,maxJerk,pickConfig,data)
        
        local pose=sim.getObjectPose(data.target,-1)
        --pose[3]=pose[3]+0.2
        moveToPose_viaIK(ikMaxVel,ikMaxAccel,ikMaxJerk,pose,data)
        --sim.wait(0.2)
        --pose[3]=pose[3]-0.2
        --moveToPose_viaIK(ikMaxVel,ikMaxAccel,ikMaxJerk,pose,data)
        
        setGripperData(false)   -- close the gripper to grasp objects, 
        sim.wait(0.5)
        
        --pose[2]=pose[2]-0.1
        pose[3]=pose[3]+0.1
        moveToPose_viaIK(ikMaxVel,ikMaxAccel,ikMaxJerk,pose,data)
        sim.wait(0.2)
        
        moveToConfig_viaFK(maxVel,maxAccel,maxJerk,destConfig,data)
        
        setGripperData(true)   -- open the gripper
        sim.wait(0.5)
        
        moveToConfig_viaFK(maxVel,maxAccel,maxJerk,destConfig2,data)  --move back to the original configuration
        sim.setObjectOrientation(data.target, data.target, {0,0,-1*graspAngle}) --orientate to original...
        sim.wait(6)
        droppedPartsCnt=droppedPartsCnt+1
    end 
    
    --moveToConfig_viaFK(maxVel,maxAccel,maxJerk,initConf,data)
    sim.wait(0.5)
    sim.stopSimulation()
end 


