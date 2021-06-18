# RoboticGraspingSimulation
To verify/test the performance of rectangle-represented grasp detection algorithms, this project builts a joint simulation environment based on the UR3 robot, RG2 gripper and a RGB-D camera.   

# Requirements  
A python interpreter, PyTorch, CoppeliaSim.  

To use the remote API functionality of Legacy Client in your Python script, you will need following 3 items:  
- sim.py  
- simConst.py  
- remoteApi.dll, remoteApi.dylib or remoteApi.so (depending on your target platform)  

Above files are located in CoppeliaSim's installation directory, under programming/remoteApiBindings/python.  

# 中文使用说明
物体模型来源 YCB model and object set - http://www.ycbbenchmarks.com/object-models/  

0、安装requirements.txt下的所有依赖包到anaconda（建议，系统python环境或其他虚拟python环境也可）  
1、打开CoppeliaSim和anaconda下的任一python编辑器  
2、将场景文件RoboticGraspingWIthUR3_v4.ttt导入CoppeliaSim  
3、在CoppeliaSim页面最下方的Lua命令行中输入simRemoteApi.start(19999)，启动Legacy服务端  
4、在python编辑器中执行文件remote_simulation.py，检测抓取位置、角度等，指导服务端抓取。  
  
P.S.   
remote_simulation.py 加载训练好的GR-convNet模型检测抓取位姿，并将相关信息传递给服务端指导抓取；  
RoboticGraspingWIthUR3_v4.ttt内部的UR3 child script实现机械臂的控制与抓取

# Instructions
