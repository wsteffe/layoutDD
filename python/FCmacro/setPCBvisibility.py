
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
     col=(255.0,170.0,127.0)
     body.ViewObject.ShapeColor=col
  if body.Label.startswith("DIEL_"):
     body.ViewObject.Transparency=80
  for item in body.Group:
    if item.Group_EnableExport:
       item.Visibility=True
#    for child in item.ViewObject.claimChildren():
#       print(f"------>{child.Label}")


#Gui.SendMsgToActiveView("ViewFit")
#Gui.updateGui( )



