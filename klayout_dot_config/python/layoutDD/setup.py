import pya

ACTIONS = []

def registerToolbarItems():

  global ACTIONS
  
  import os
  from  importlib import reload 
  from . import loaders
  reload(loaders)
  from . import subdomains
  reload(subdomains)

  menu = pya.Application.instance().main_window().menu()
  act = pya.Action()

  s1 = "layoutDD"
  if not(menu.is_menu(s1)):
     menu.insert_menu("help_menu", s1, "layoutDD")

  act = pya.Action()
  act.title = "import DXF"
  act.on_triggered(loaders.importDXF)
  menu.insert_item(s1+".begin", "ImportDXF", act)
  ACTIONS.append(act)

  act = pya.Action()
  act.title = "Open DD Project"
  act.on_triggered(loaders.openProject)
  menu.insert_item(s1+".ImportDXF+", "openProject", act)
  ACTIONS.append(act)

  act = pya.Action()
  act.title = "Create New Region"
  act.on_triggered(subdomains.newRegion)
  menu.insert_item(s1+".openProject+", "newRegion", act)
  ACTIONS.append(act)




