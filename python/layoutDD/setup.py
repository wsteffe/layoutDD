import pya
import sys

ACTIONS = []
layerMap=None

def installRequirements():
   import importlib.util
   import pip
   import sys
   import os
   reqPath  = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "requirements.txt"))
   required = set()
   with open(reqPath) as reqfile:
      for line in reqfile:
         line=line.split("#")[0]
         line=line.rstrip()
         if len(line)>0:
             required.add(line)
   for package in required:
      if importlib.util.find_spec(package) is None:
         pya.MessageBox.info("Information", "Installing "+package+" with pip", pya.MessageBox.Ok)
         pip.main(['install', package])


def installFreeCAD_():
    import os
    from git import Repo
    repo_url="https://github.com/wsteffe/layoutDD_FreeCAD"
    username = os.getenv("USERNAME")
    installPath="c:/users/"+username+"/AppData/Roaming/layoutDD_FreeCAD"
    repo = Repo.clone_from(repo_url, installPath)


def installFreeCAD():
    import tempfile,requests,os,zipfile
    zipurl="https://github.com/wsteffe/klayout_FreeCAD/archive/refs/tags/v1.0.zip"
    username = os.getenv("USERNAME")
    installPath="c:/users/"+username+"/AppData/Roaming/"
    zip_path=None
    with tempfile.NamedTemporaryFile(delete=False) as tmpf:
       zip_path=tmpf.name
       with requests.get(zipurl) as r:
          r.raise_for_status()
          for chunk in r.iter_content(chunk_size=512 * 1024): 
              if chunk: # filter out keep-alive new chunks
                 tmpf.write(chunk)
    with zipfile.ZipFile(zip_path, "r") as f:
       f.extractall(installPath)
    os.rename(installPath+"klayout_FreeCAD-1.0/bin",installPath+"KLayout/bin")
    os.rename(installPath+"klayout_FreeCAD-1.0/Ext",installPath+"KLayout/Ext")
    os.rename(installPath+"klayout_FreeCAD-1.0/Mod",installPath+"KLayout/Mod")
    os.remove(installPath+"klayout_FreeCAD-1.0/*")
    os.rmdir(installPath+"klayout_FreeCAD-1.0")
    os.remove(zip_path)

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

  if sys.platform=="win32":
     act = pya.Action()
     act.title = "Install Python Dependencies"
     act.on_triggered(installRequirements)
     menu.insert_item(s1+".makeSubdomain+", "installRequirements", act)
     ACTIONS.append(act)

     act = pya.Action()
     act.title = "Install FreeCAD"
     act.on_triggered(installFreeCAD)
     menu.insert_item(s1+".installRequirements+", "installFreeCAD", act)
     ACTIONS.append(act)









