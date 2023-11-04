import pya

ACTIONS = []
layerMap=None

def registerToolbarItems():

  global ACTIONS
  
  import os
  from  importlib import reload 
  import loaders
  reload(loaders)
  import subdomains
  reload(subdomains)
  import globalVar
  reload(globalVar)

  menu = pya.Application.instance().main_window().menu()
  act = pya.Action()

  s1 = "layoutDD"
  if not(menu.is_menu(s1)):
     menu.insert_menu("help_menu", s1, "layoutDD")

  act = pya.Action()
  act.title = "Import Layout"
  act.on_triggered(loaders.importLayout)
  menu.insert_item(s1+".begin", "ImportLayout", act)
  ACTIONS.append(act)

  act = pya.Action()
  act.title = "Open DD Project"
  act.on_triggered(loaders.openProject)
  menu.insert_item(s1+".ImportLayout+", "openProject", act)
  ACTIONS.append(act)

  act = pya.Action()
  act.title = "New Region"
  act.on_triggered(subdomains.newRegion)
  menu.insert_item(s1+".openProject+", "newRegion", act)
  ACTIONS.append(act)

  act = pya.Action()
  act.title = "New WGP in Region"
  act.on_triggered(subdomains.newWGP)
  menu.insert_item(s1+".newRegion+", "newWGP", act)
  ACTIONS.append(act)

  act = pya.Action()
  act.title = "Edit Region Stack"
  act.on_triggered(subdomains.editRegion)
  menu.insert_item(s1+".newWGP+", "editRegion", act)
  ACTIONS.append(act)

  act = pya.Action()
  act.title = "Edit WGP"
  act.on_triggered(subdomains.editWGP)
  menu.insert_item(s1+".editRegion+", "editWGP", act)
  ACTIONS.append(act)

  act = pya.Action()
  act.title = "Delete Region"
  act.on_triggered(subdomains.deleteRegion)
  menu.insert_item(s1+".editWGP+", "deleteRegion", act)
  ACTIONS.append(act)

  act = pya.Action()
  act.title = "Delete WGP"
  act.on_triggered(subdomains.deleteWGP)
  menu.insert_item(s1+".deleteRegion+", "deleteWGP", act)
  ACTIONS.append(act)

  act = pya.Action()
  act.title = "Make Subdomain"
  act.on_triggered(subdomains.makeSubdomain)
  menu.insert_item(s1+".deleteWGP+", "makeSubdomain", act)
  ACTIONS.append(act)






