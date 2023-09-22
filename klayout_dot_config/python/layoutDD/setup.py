import pya

ACTIONS = []

def registerToolbarItems():

  global ACTIONS
  
  import os
  from  importlib import reload 
  from . import importPCB
  reload(importPCB)

  menu = pya.Application.instance().main_window().menu()
  act = pya.Action()

  s1 = "layoutDD"
  if not(menu.is_menu(s1)):
     menu.insert_menu("help_menu", s1, "layoutDD")

  act = pya.Action()
  act.title = "import PCB"
  act.on_triggered(importPCB.importPCB)
  menu.insert_item(s1+".begin", "import PCB", act)
  ACTIONS.append(act)



