'''
FILE demo-helloJoy.py

This demonstrates basic joyapp programming and it converts your mouse postion to y-value and prints it on your screen
'''
from joy.decl import *
from joy import JoyApp

class HelloJoyApp( JoyApp ):
  """HelloJoyApp

     The "hello world" of JoyApp programming.
     This JoyApp pipes the y coordinate of mouse positions (while left
     button is pressed) to a specified setter. By default this setter is
     given by "#output " -- i.e. it is a debug message.

     See JoyApp.setterOf() for a specification of possible outputs

     This file is intended to introduce you to our joy library
  """
  def __init__(self,robot = dict(count=3),*arg,**kw):

    JoyApp.__init__(self,robot = robot, *arg,**kw)
    self.nx17_pos = self.robot.at.Nx17.get_pos()
    self.nx10_pos = self.robot.at.Nx10.get_pos()
    # self.1E_keep_moving = False


  def onStart(self):
    progress("Start")

  def onStop(self):
    progress("Stop")

  def angle_limit_check(self,input_angle):
    if (input_angle > 9700 ):
      progress("---------------------------")
      progress("WARNING: ANGLE LIMIT ACHIEVEDC")
      progress("---------------------------")
      return 9700
    elif (input_angle < -9700):
      progress("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      progress("WARNING: ANGLE LIMIT ACHIEVEDC")
      progress("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      return -9700
    else:
      return input_angle
  
  def onEvent(self,evt):
    progress("----------")
    
    offset_1 = 500
    offset_2 = 500
    progress("10 pos: "+str(self.nx10_pos))
    progress("17 pos: "+str(self.nx17_pos))
    if (evt.type == KEYDOWN):
      # keyboard input
      # print(str(evt.key))
      if (evt.key == K_w ):
        self.nx10_pos = self.angle_limit_check(self.nx10_pos + offset_1)
        self.robot.at.Nx10.set_pos( self.nx10_pos)
      elif (evt.key == K_s):
        self.nx10_pos = self.angle_limit_check(self.nx10_pos - offset_1)
        self.robot.at.Nx10.set_pos(self.nx10_pos)
      elif (evt.key == K_e):
        self.nx17_pos = self.angle_limit_check(self.nx17_pos + offset_2)
        self.robot.at.Nx17.set_pos(self.nx17_pos)
      elif (evt.key == K_d):
        self.nx17_pos = self.angle_limit_check(self.nx17_pos - offset_2)
        self.robot.at.Nx17.set_pos(self.nx17_pos)
      elif (evt.key == K_LEFTBRACKET):
        # "[" to stop
        self.stop()
      else:
        pass
      

if __name__=="__main__":
  app = HelloJoyApp(robot=dict(count=2))
  app.run()
