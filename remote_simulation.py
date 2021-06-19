#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 21:28:46 2021

@author: marco
"""

import sim
#import sys
import numpy as np
#import math
#import matplotlib.pyplot as plt
from inference_by_python import inference
#import time
#import cv2


'''******IMPOTRANT******
simRemoteApi.start(19999) -- input this line in Lua command of simulation firstly'''

sim.simxFinish(-1)  # Just in case, close all opened connections
sim_client = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if sim_client == -1:
    print('Failed to connect to simulation (V-REP remote API server). Exiting.')
    exit()
else:
    print('Connected to simulation.')
    
# Synchronously Running the client and server
sim.simxSynchronous(sim_client,True); # Enable the synchronous mode (Blocking function call)
sim.simxStartSimulation(sim_client,sim.simx_opmode_oneshot)
sim.simxSynchronousTrigger(sim_client)  #trigger the simulation 

sim_ret, rgb_cam = sim.simxGetObjectHandle(sim_client, "kinect_rgb", sim.simx_opmode_blocking)
sim_ret, depth_cam = sim.simxGetObjectHandle(sim_client, "kinect_depth", sim.simx_opmode_blocking)

#Wait for Signal objectNumber
err, objectNumber=sim.simxGetIntegerSignal(sim_client,'objectNumber',sim.simx_opmode_streaming) 
while err != sim.simx_return_ok:
  err,objectNumber=sim.simxGetIntegerSignal(sim_client,'objectNumber',sim.simx_opmode_buffer)
print(r'objectNumber: %i.'%(objectNumber))	
sim.simxClearIntegerSignal(sim_client,'objectNumber',sim.simx_opmode_oneshot)

#x=[0.375,0.250,0.35]
#y=[0.050,0.050,0.15]
#angle=[30*math.pi/180,0,0]

for i in range(objectNumber):
    
    #Wait for Signal sendImages
    err2, sendImages=sim.simxGetStringSignal(sim_client,'sendImages',sim.simx_opmode_streaming)
    while err2 != sim.simx_return_ok:
        err2,sendImages=sim.simxGetStringSignal(sim_client,'sendImages',sim.simx_opmode_buffer)
    print(r'sendImages: %s' %(sendImages))
    sim.simxClearStringSignal(sim_client,'sendImages', sim.simx_opmode_oneshot)

    # Acquire RGB Image
    sim_ret, resolution, raw_image = sim.simxGetVisionSensorImage(sim_client, rgb_cam, 0, sim.simx_opmode_blocking)
    color_img = np.asarray(raw_image)
    color_img.shape = (resolution[1], resolution[0],3)
    color_img = color_img.astype(np.float)
    color_img[color_img < 0] += 255
    color_img = np.flipud(color_img)
    color_img = color_img.astype(np.uint8)
    
    # Gain Depth Image
    sim_ret, resolution, depth_buffer = sim.simxGetVisionSensorDepthBuffer(sim_client, depth_cam, sim.simx_opmode_blocking)
    depth_img = np.asarray(depth_buffer)
    #depth_img= cv2.rgb2grey
    depth_img.shape = (resolution[1], resolution[0])
    depth_img = np.flipud(depth_img)
    depth_img = depth_img * 255
    #zNear = 0.01
    #zFar = 2
    #depth_img = depth_img0 * (zFar - zNear) + zNear
    
    
    #Inference by Deep Learning model
    #X=x[i]
    #Y=y[i]
    #graspAngle=angle[i]
    
    args_network='/home/marco/vrep_python/trained-models/cornell-randsplit-rgbd-grconvnet3-drop1-ch32/epoch_19_iou_0.98'
    args_use_depth=True
    args_use_rgb=True
    args_n_grasps=1
    args_save=True
    args_force_cpu=False
    grasps=inference(args_network, color_img,depth_img,args_use_depth,args_use_rgb, args_n_grasps,args_save,args_force_cpu)
    
    X=grasps[0].center[0]*0.5/223
    Y=grasps[0].center[1]*0.5/223
    graspAngle=grasps[0].angle
    local_depth_min=np.max(depth_img)
    for  a in range(grasps[0].center[0]-6,grasps[0].center[0]+7):
        row_min=np.min(depth_img[a][(grasps[0].center[1]-6):(grasps[0].center[1]+7)])
        if row_min<local_depth_min:
            local_depth_min=row_min
            
    #depth_grasp=depth_img[grasps[0].center[0]][grasps[0].center[1]]
    #graspCenterZ=(0.46175-0.02)*(1-np.min(depth_img)/np.max(depth_img))-0.05
    graspCenterZ=(0.46175-0.02)*(1-local_depth_min/np.max(depth_img))-0.05
    #grasps.quality, grasps.width, grasps.length
    
    # send grasps to CoppeliaSim that should be received and evaluated at the same time
    sim.simxPauseCommunication(sim_client,True)
    sim.simxSetFloatSignal(sim_client,'graspCenterX', X, sim.simx_opmode_oneshot)
    sim.simxSetFloatSignal(sim_client,'graspCenterY', Y, sim.simx_opmode_oneshot)
    sim.simxSetFloatSignal(sim_client,'graspAngle', graspAngle, sim.simx_opmode_oneshot)
    sim.simxSetFloatSignal(sim_client,'graspCenterZ', graspCenterZ, sim.simx_opmode_oneshot)
    sim.simxSetStringSignal(sim_client,'sendGrasps', 'start', sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(sim_client,False)
    #Above's 3 values will be received on the CoppeliaSim side at the same time
    
    '''
    plt.figure(2*i)
    plt.imshow(color_img)
    #saveimg
    plt.figure(2*i+1)
    plt.imshow(depth_img) #
    #saveimg
    '''