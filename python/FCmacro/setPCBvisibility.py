
import Part
import FreeCAD

doc=App.ActiveDocument
parts = [obj for obj in doc.Objects if obj.isDerivedFrom("App::Part")]
for part in parts:
  part.Visibility=True
bodies = [obj for obj in doc.Objects if obj.isDerivedFrom("PartDesign::Body")]
for body in bodies:
  body.Visibility=True
  if body.Label.startswith("BC_"):
     col=(255,170,127)
     body.ViewObject.ShapeColor=col
  if body.Label.startswith("WGP_"):
     col=(255,0,0)
     body.ViewObject.ShapeColor=col
     body.ViewObject.Transparency=0
  if body.Label.startswith("DIEL_"):
     body.ViewObject.Transparency=80
  for item in body.Group:
    if item.Group_EnableExport:
       item.Visibility=True
       
features = [obj for obj in doc.Objects if obj.isDerivedFrom("Part::Feature")]
for feature in features:
  feature.Visibility=True
  if feature.Label.startswith("BC_"):
     col=(255,170,127)
     feature.ViewObject.ShapeColor=col
  if feature.Label.startswith("WGP_"):
     col=(255,0,0)
     feature.ViewObject.ShapeColor=col
     feature.ViewObject.Transparency=0
  if feature.Label.startswith("DIEL_"):
     feature.ViewObject.Transparency=80


#    for child in item.ViewObject.claimChildren():
#       print(f"------>{child.Label}")


#Gui.SendMsgToActiveView("ViewFit")
#Gui.updateGui( )



