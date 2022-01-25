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
    # self.1E_keep_moving = False


  def onStart(self):
    progress("Start")

  def onStop(self):
    progress("Stop")

  # def w_function(self):
  #   # move 5 steps forward
  #   if (self.1E_keep_moving):
  #     self.1E_keep_moving = False
  #   else:
  #     self.robot.at.Nx1E.set_pos(6000)
  
  def onEvent(self,evt):
    progress("----------")
    # nx17_pos = self.robot.at.Nx17.get_pos()
    nx1E_pos = self.robot.at.Nx1E.get_pos()
    progress("1E pos: "+str(nx1E_pos))
    # nx10_pos = robot.Nx10.get_pos()
    # nx17_pos = robot.Nx17.get_pos()
    # progress(str(evt.type) +str(evt.key))
    if (evt.type == KEYDOWN):
      # keyboard input
      if (evt.key == K_w ):
        # self.robot.at.Nx17.set_pos(nx17_pos + 500)
        self.robot.at.Nx1E.set_pos(nx1E_pos + 500)
      elif (evt.key == K_s):
        # self.robot.at.Nx17.set_pos(nx17_pos - 500)
        self.robot.at.Nx1E.set_pos(nx1E_pos - 500)
      

if __name__=="__main__":
  app = HelloJoyApp(robot=dict(count=1))
  app.run()
