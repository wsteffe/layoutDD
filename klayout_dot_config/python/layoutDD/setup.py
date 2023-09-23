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


  act = pya.Action()
  act.title = "Open DD Project"
  act.on_triggered(importDXF.openProject)
  menu.insert_item(s1+".ImportDXF+", "openProject", act)
  ACTIONS.append(act)



