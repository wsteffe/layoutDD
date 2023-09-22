import pya

ACTIONS = []

def registerToolbarItems():

  global ACTIONS
  
  import os
  from . import mapLayers

  menu = pya.Application.instance().main_window().menu()
  act = pya.Action()

  s1 = "layoutDD"
  if not(menu.is_menu(s1)):
     menu.insert_menu("help_menu", s1, "layoutDD")

  act = pya.Action()
  act.title = "mapLayers"
  act.on_triggered(mapLayers.mapLayers)
  menu.insert_item(s1+".begin", "mapLayers", act)
  ACTIONS.append(act)



