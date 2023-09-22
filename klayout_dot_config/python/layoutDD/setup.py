import pya

ACTIONS = []

def registerToolbarItems():

  global ACTIONS
  
  import os
  from  importlib import reload 
  from . import importDXF
  reload(importDXF)

  menu = pya.Application.instance().main_window().menu()
  act = pya.Action()

  s1 = "layoutDD"
  if not(menu.is_menu(s1)):
     menu.insert_menu("help_menu", s1, "layoutDD")

  act = pya.Action()
  act.title = "import DXF"
  act.on_triggered(importDXF.importDXF)
  menu.insert_item(s1+".begin", "ImportDXF", act)
  ACTIONS.append(act)


#  act = pya.Action()
#  act.title = "Save Active Cell"
#  act.on_triggered(saveActiveCell.saveActiveCell)
#  menu.insert_item(s1+".ImportDXF+", "SaveActiveCell", act)
#  ACTIONS.append(act)



