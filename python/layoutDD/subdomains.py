import pya

from pya import *
import sys 

# creating a class 
# that inherits the QDialog class 
class ZextentDialog(pya.QDialog): 

  # Dialog constructor 
  def __init__(self, REGION_KEY,stack, parent = None): 
      pya.QDialog.__init__(self)

      self.REGION_KEY=REGION_KEY
      self.stack=stack

      # setting window title 
      self.setWindowTitle("Region Z extent") 

      # setting geometry to the window 
      self.setGeometry(100, 100, 100, 100) 

      # creating a group box 
      self.formGroupBox = QGroupBox(REGION_KEY+" z extent") 
      vb = pya.QVBoxLayout(self.formGroupBox)

      #Create Labels
      self.z1 = QLabel('Zstart')
      self.z2 = QLabel('Zend')       

      # creating a line edit 
      self.nameLineEdit1 = QLineEdit(self.formGroupBox)
      vb.addWidget(self.z1)
      vb.addWidget(self.nameLineEdit1)
      self.nameLineEdit2 = QLineEdit(self.formGroupBox)
      vb.addWidget(self.z2)
      vb.addWidget(self.nameLineEdit2)
      if REGION_KEY in stack:
        self.nameLineEdit1.setText(stack[REGION_KEY][0])
        self.nameLineEdit2.setText(stack[REGION_KEY][1])

      # creating a dialog button for ok and cancel 
      self.buttonBox = QDialogButtonBox(self)#.new_buttons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
      #self.buttonBox.buttonRole(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
      self.ok = self.buttonBox.addButton(QDialogButtonBox.Ok)
      self.cancel = self.buttonBox.addButton(QDialogButtonBox.Cancel)

      #(self.buttonBox.)

      # adding action when form is accepted 
      self.cancel.clicked(lambda button: self.reject())

      # addding action when form is rejected 
      self.ok.clicked(self.getInfo)

      # creating a vertical layout 
      mainLayout = QVBoxLayout() 

      # adding form group box to the layout 
      mainLayout.addWidget(self.formGroupBox) 

      # adding button box to the layout 
      mainLayout.addWidget(self.buttonBox) 

      # setting lay out 
      self.setLayout(mainLayout) 

  # get info method called when form is accepted 
  def getInfo(self): 
      # printing the form information 
      self.stack[self.REGION_KEY]=[self.nameLineEdit1.text,self.nameLineEdit2.text]
      # closing the window 
      self.close()




def newRegion():
    import os
    from . import loaders,globalVar

    mainWindow   = pya.Application.instance().main_window()
    layoutView   = pya.Application.instance().main_window().current_view()
    cellView     = layoutView.cellview(1)
    cellViewI    = cellView.index()
    cellLayout   = cellView.layout()
    REGION_KEY="Region_1"

    if len(globalVar.partition_stack)>0:
        REGION_KEY= "Region_"+str(1+max( [int(k.split('_')[1]) for k in globalVar.partition_stack.keys()]))

    GUI_Klayout = ZextentDialog(REGION_KEY,globalVar.partition_stack,pya.Application.instance().main_window())
    GUI_Klayout.exec_()

    loaders.saveStack('partition.stack',globalVar.partition_stack)

    cell         = cellLayout.create_cell(REGION_KEY)
    cellLayer    = cellLayout.layer(0,0)
    cellView.cell= cell
    option       = pya.SaveLayoutOptions()
    layoutView   = mainWindow.current_view()
    layoutView.add_missing_layers()
    layoutView.save_as(cellViewI,f"partition.gds", option)


def name2index(name):
    I=0
    l=len(name)
    for i in range(l):
       if name[-(i+1):].isdigit():
         I=int(name[-(i+1):])
       else:
         exit
    return str(I)

def editRegion():
    import os
    from . import loaders,globalVar

    mainWindow   = pya.Application.instance().main_window()
    layoutView   = pya.Application.instance().main_window().current_view()
    cellView     = layoutView.cellview(1)
    cell         = cellView.cell
    cellLayout   = cellView.layout()
    REGION_KEY=cell.name

    GUI_Klayout = ZextentDialog(REGION_KEY,globalVar.partition_stack,pya.Application.instance().main_window())
    GUI_Klayout.exec_()
#    print("Zstart : {0}".format(partition_stack[REGION_KEY][0])) 
#    print("Zend : {0}".format(partition_stack[REGION_KEY][1]))         

    loaders.saveStack('partition.stack',globalVar.partition_stack)


def newWGP():
    import os
    from . import saveActiveCell,loaders,globalVar
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = mainWindow.current_view()
    cellView     = layoutView.cellview(1)
    cellViewId   = cellView.index()
    cell         = cellView.cell
    cellLayout   = cellView.layout()
    REGION_KEY=cell.name
    wgp_keys = [ k for k in globalVar.partition_stack.keys() if k.startswith(REGION_KEY) and len(k.split('_'))>3]
    WGI=1
    if len(wgp_keys)>0:
        WGI=1+max([int(k.split('_')[3]) for k in wgp_keys])
    WGP_KEY= "WGP_"+str(WGI)
    GUI_Klayout = ZextentDialog(REGION_KEY+"_"+WGP_KEY,globalVar.partition_stack,pya.Application.instance().main_window())
    GUI_Klayout.exec_()
    loaders.saveStack('partition.stack',globalVar.partition_stack)
    cellv_lid =cellLayout.layer(WGI, 0)
    cellv_lif =cellLayout.get_info(cellv_lid)
    if cellv_lif.name!=WGP_KEY:
       cellv_lif.name= WGP_KEY
       cellLayout.set_info(cellv_lid,cellv_lif)
       option       = pya.SaveLayoutOptions()
       layoutView   = mainWindow.current_view()
       layoutView.add_missing_layers()
       saveActiveCell.saveActiveCell()


def editWGP():
    import os
    from . import saveActiveCell,loaders,globalVar
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = mainWindow.current_view()
    cellView     = layoutView.cellview(1)
    cellViewId   = cellView.index()
    cell         = cellView.cell
    cellLayout   = cellView.layout()
    REGION_KEY=cell.name
    lyp=layoutView.current_layer.current()
    if lyp.cellview()!=cellViewId:
        return
    lid = lyp.layer_index()
    if lid<0:
        return
    cellv_lif = cellLayout.get_info(lid)
    WGI,dt = cellv_lif.layer, cellv_lif.datatype
    WGP_KEY= "WGP_"+str(WGI)
    wgp_keys = [ k for k in globalVar.partition_stack.keys() if k.startswith(REGION_KEY) and len(k.split('_'))>3]
    k=REGION_KEY+"_"+WGP_KEY
    if k not in wgp_keys:
        return
    GUI_Klayout = ZextentDialog(k,globalVar.partition_stack,pya.Application.instance().main_window())
    GUI_Klayout.exec_()
    loaders.saveStack('partition.stack',globalVar.partition_stack)


def deleteWGP():
    import os
    from . import saveActiveCell,loaders,globalVar
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = mainWindow.current_view()
    cellView     = layoutView.cellview(1)
    cellViewId   = cellView.index()
    cell         = cellView.cell
    cellLayout   = cellView.layout()
    REGION_KEY=cell.name
    lyp=layoutView.current_layer.current()
    if lyp.cellview()!=cellViewId:
        return
    lid = lyp.layer_index()
    if lid<0:
        return
    cellv_lif = cellLayout.get_info(lid)
    WGI,dt = cellv_lif.layer, cellv_lif.datatype
    WGP_KEY= "WGP_"+str(WGI)
    wgp_keys = [ k for k in globalVar.partition_stack.keys() if k.startswith(REGION_KEY) and len(k.split('_'))>3]
    k=REGION_KEY+"_"+WGP_KEY
    if k not in wgp_keys:
        return
    del globalVar.partition_stack[k]
    cell.clear(lid)
    saveActiveCell.saveActiveCell()
    loaders.saveStack('partition.stack',globalVar.partition_stack)


def deleteRegion():
    import os
    from . import loaders, globalVar

    mainWindow   = pya.Application.instance().main_window()
    layoutView   = pya.Application.instance().main_window().current_view()
    cellView     = layoutView.cellview(1)
    cell         = cellView.cell
    cellLayout   = cellView.layout()
    REGION_KEY=cell.name
    cellI=cell.cell_index()
    cellLayout.delete_cell(cellI)
    region_keys = [ k for k in globalVar.partition_stack.keys() if k.startswith(REGION_KEY)]
    if region_keys:
      for k in region_keys:
        del globalVar.partition_stack[k]
      loaders.saveStack('partition.stack',globalVar.partition_stack)


def interceptedLayer(layerName,cellName):
    from . import globalVar
    if layerName not in globalVar.stack:
        return False
    if cellName not in globalVar.partition_stack:
        return False
    [prefix,z0,z1,op,order]=globalVar.stack[layerName]
    [cell_z0,cell_z1]=globalVar.partition_stack[cellName]
    return z0<=cell_z1 and z1>=cell_z0


def copyInterceptedLayers(layoutView):
    from . import saveActiveCell, globalVar
    mainCellView  = layoutView.cellview(0)
    mainCellViewId = mainCellView.index()
    cellView       = layoutView.active_cellview()
    cellViewId     = cellView.index()
    if cellViewId==mainCellViewId:
        return
    mainFilePath      = mainCellView.filename()
    mainFilePathSeg   = mainFilePath.replace("\\", "/").split("/")
    mainFname         = mainFilePathSeg[-1].split(".")[0]
    mainLayout= mainCellView.layout()
    cellLayout= cellView.layout()
    cell = cellView.cell
    if cell is None:
       return
    [cell_z0,cell_z1]=globalVar.partition_stack[cell.name]
    cell_z0=float(cell_z0)
    cell_z1=float(cell_z1)
    for lyp in layoutView.each_layer():
       lid = lyp.layer_index()
       if lid<0:
           continue
       if lyp.source_name=="none":
           continue
       if lyp.cellview()==cellViewId and lyp.visible:
          cellv_lif = cellLayout.get_info(lid)
          ln,dt = cellv_lif.layer, cellv_lif.datatype
          if (ln,dt)==(0,1):
             lyp.visible=False
       if lyp.cellview()==mainCellViewId:
          if lyp.source_name not in globalVar.stack:
            continue
          [prefix,z0,z1,op,order]=globalVar.stack[lyp.source_name]
          z0=float(z0)
          z1=float(z1)
          if z0>cell_z1 or z1<cell_z0:
            continue
          lif = mainLayout.get_info(lid)
          ln,dt = lif.layer, lif.datatype
          if (ln,dt)==(0,0):
             continue
          cellv_lid = cellLayout.layer(ln, dt)
          cellv_lif = cellLayout.get_info(cellv_lid)
          cellv_lif.name= lyp.source_name
          cellLayout.set_info(cellv_lid,cellv_lif)
    layoutView.add_missing_layers()
    saveActiveCell.saveActiveCell()


def getCellLayers(layoutView):
    mainCellView   = layoutView.cellview(0)
    mainCellViewId = mainCellView.index()
    cellView       = layoutView.active_cellview()
    cellViewId     = cellView.index()
    cellLayout= cellView.layout()
    cellLayers=set()
    cell =cellView.cell
    if cellViewId==mainCellViewId:
       return
    if cell is None:
       return cellLayers
    for lyp in layoutView.each_layer():
       if lyp.cellview()==cellViewId:
          lid = lyp.layer_index()
          if lid<0:
             continue
          lif = cellLayout.get_info(lid)
          ln,dt = lif.layer, lif.datatype
          if ln==0:
             continue
          if len(lif.name)==0:
              continue
          cellLayers.add(lif.name)
    return cellLayers

def new_FCdocument(path):
    import FreeCAD
    import Part
    doc = FreeCAD.newDocument()
    doc.saveAs(path+'.FCStd')
    if hasattr(Part, 'disableElementMapping'):
        Part.disableElementMapping(doc)
    doc.UndoMode = 0
    return doc

def evalLayerRegion(lname):
   layoutView  = pya.Application.instance().main_window().current_view()
   mainCellView = layoutView.cellview(0)
   mainCellViewId = mainCellView.index()
   mainLayout= mainCellView.layout()
   mainCell = mainCellView.cell
   layerReg=None
   for lyp in layoutView.each_layer():
     if lyp.cellview()==mainCellViewId:
       lid = lyp.layer_index()
       if lid<0:
           continue
       if lyp.source_name!=lname:
           continue
       layerReg =pya.Region([itr.shape().polygon.transformed(itr.trans()) for itr in mainLayout.begin_shapes(mainCell, lid)])
   return layerReg

def pointIsInLayerRegion(x,y,layerReg):
   box = pya.Box(x-1, y-1, x+1, y+1)
   region_b = pya.Region(box)
   result = layerReg.interacting(region_b)
   if not result.is_empty():
      return True
   else:
      return False

def getPointInFace(face,importFac):
    import FreeCAD
    import Part
    surf =face.Surface
    u0, u1, v0, v1 = surf.bounds()
    u = (u0 + u1)/2
    v = (v0 + v1)/2
    n= surf.normal(u, v)
#    n = face.normalAt(0,0)
    if face.Wires:
        edges=face.Wires[0].Edges
        orientation=face.Wires[0].Orientation
    else:
        edges=face.Edges
        orientation="Forward"
    minRadius=10.e10
    eddgeMinR=None
    for edge in edges:
        sgn=1 if edge.Orientation == orientation else -1
        if isinstance(edge.Curve, Part.Circle):
           if edge.Closed:
               return edge.Curve.Center
           elif edge.Curve.Radius<minRadius:
               minRadius=edge.Curve.Radius
               eddgeMinR=edge
        if isinstance(edge.Curve,(Part.Line, Part.LineSegment)):
           t = edge.Curve.tangent((edge.ParameterRange[0]+edge.ParameterRange[1])/2)[0]
           p = edge.Curve.value((edge.ParameterRange[0]+edge.ParameterRange[1])/2)
           bn=n.cross(t)
           return p+sgn*bn*2/importFac
    if eddgeMinR:
        t = eddgeMinR.Curve.tangent((eddgeMinR.ParameterRange[0]+eddgeMinR.ParameterRange[1])/2)[0]
        p = eddgeMinR.Curve.value((eddgeMinR.ParameterRange[0]+eddgeMinR.ParameterRange[1])/2)
        bn=n.cross(t)
        return p+sgn*bn*2/importFac
    return None

def mergeLayerFaces(layerFaces):
    from BOPTools.ShapeMerge import mergeShapes
    msh=mergeShapes(layerFaces)
    layerFaces=[]
    for shell in msh.Shells:
      face=None
      if len(shell.Faces)>1:
        fsh=shell.Faces[0].fuse(shell.Faces[1:])
        rsh=fsh.removeSplitter()
        if len(rsh.Faces)==1:
          face=rsh.Faces[0]
        else:
          face=rsh.Faces
      elif shell.Faces:
        face=shell.Faces[0]
      if face:
        layerFaces.append(face)
    return layerFaces


def makeLayerFaces1(lname,FCclipShape,FClayerShape,importFac,useAllClipPoly=False):
    import FreeCAD
    import Part
    from BOPTools.GeneralFuseResult import GeneralFuseResult
    contWire=Part.Wire(FCclipShape.Edges)
    face=Part.Face(contWire)
    if useAllClipPoly:
       layerFaces=[face]
       return layerFaces
    layerReg=evalLayerRegion(lname)
    hasFClayerEdges=False
    if FClayerShape:
        if FClayerShape.Edges:
            hasFClayerEdges=True
    if not hasFClayerEdges:
       cedge=FCclipShape.Edges[0]
       P1=cedge.Vertexes[0].Point
       P2=cedge.Vertexes[1].Point
       Pc=(P1+P2)/2
       xc=Pc[0]*importFac
       yc=Pc[1]*importFac
       layerFaces=[]
       if layerReg != None:
          if pointIsInLayerRegion(xc,yc,layerReg):
             layerFaces.append(face)
    else:
       shapes=[face]
       NcontEdges=0
       for edge in FCclipShape.Edges:
         shapes.append(edge)
         NcontEdges=NcontEdges+1
       for edge in FClayerShape.Edges:
         shapes.append(edge)
       tolerance=0.0
       pieces, map = shapes[0].generalFuse(shapes[1:], tolerance)          
       gr =GeneralFuseResult(shapes, (pieces,map))
       slicedFace=gr.piecesFromSource(shapes[0])
       tbdFaceSet=set()
       for face in slicedFace:
         tbdFaceSet.add(face)
         p=getPointInFace(face,importFac)
       slicedContour=[]
       for i in range(NcontEdges):
         slicedEdge=gr.piecesFromSource(shapes[i+1])
         if len(slicedEdge)>0:
           for edge in slicedEdge:
             slicedContour.append(edge)
         else:
           slicedContour.append(shapes[i+1])
       keepFaceSet=set()
       rmFaceSet=set()
       for cedge in slicedContour:
          P1=cedge.Vertexes[0].Point
          P2=cedge.Vertexes[1].Point
          Pc=(P1+P2)/2
          xc=Pc[0]*importFac
          yc=Pc[1]*importFac
          for face in slicedFace:
            found=False
            if face in tbdFaceSet and not found:
               for edge in face.Edges:
                   if edge.isSame(cedge):
                     if pointIsInLayerRegion(xc,yc,layerReg):
                         keepFaceSet.add(face)
                     else:
                         rmFaceSet.add(face)
                         tbdFaceSet.remove(face)
                         found=True
                         break
       maxNestLevel=1
       nestLevel=0
       rmFaceSet1=rmFaceSet
       while tbdFaceSet and nestLevel<maxNestLevel:
         nestLevel=nestLevel+1
         keepFaceSet1=set()
         for rface in rmFaceSet1:
            for rfwire in rface.Wires:
               for face in tbdFaceSet:
                 if face not in keepFaceSet:
                    for wire in face.Wires:
                       if wire.isSame(rfwire):
                           keepFaceSet.add(face)
                           keepFaceSet1.add(face)
            for redge in rface.Edges:
               if redge.isClosed():
                  for face in tbdFaceSet:
                     if face not in keepFaceSet:
                        for edge in face.Edges:
                           if edge.isSame(redge):
                               keepFaceSet.add(face)
                               keepFaceSet1.add(face)
            for face in keepFaceSet1:
               if face in tbdFaceSet:
                    tbdFaceSet.remove(face)
         rmFaceSet1=set()
         for kface in keepFaceSet1:
            for kwire in kface.Wires:
               for face in tbdFaceSet:
                   if face not in rmFaceSet:
                      for wire in face.Wires:
                         if wire.isSame(kwire):
                            rmFaceSet.add(face)
                            rmFaceSet1.add(face)
            for kedge in kface.Edges:
               if kedge.isClosed():
                  for face in tbdFaceSet:
                     if face not in rmFaceSet:
                        for edge in face.Edges:
                           if edge.isSame(kedge):
                              rmFaceSet.add(face)
                              rmFaceSet1.add(face)
            for face in rmFaceSet1:
               if face in tbdFaceSet:
                   tbdFaceSet.remove(face)
       layerFaces=[ f for f in keepFaceSet]
       layerFaces=mergeLayerFaces(layerFaces)
    return layerFaces


def makeLayerFaces2(lname,FCclipShape,FClayerShape,importFac,useAllClipPoly=False):
    import FreeCAD
    import Part
    from BOPTools.GeneralFuseResult import GeneralFuseResult
    from . import globalVar
    contWire=Part.Wire(FCclipShape.Edges)
    face=Part.Face(contWire)
    if useAllClipPoly:
       layerFaces=[face]
       return layerFaces
    layerReg=evalLayerRegion(lname)
    hasFClayerEdges=False
    if FClayerShape:
        if FClayerShape.Edges:
            hasFClayerEdges=True
    if not hasFClayerEdges:
       cedge=FCclipShape.Edges[0]
       P1=cedge.Vertexes[0].Point
       P2=cedge.Vertexes[1].Point
       Pc=(P1+P2)/2
       xc=Pc[0]*importFac
       yc=Pc[1]*importFac
       layerFaces=[]
       if layerReg != None:
          if pointIsInLayerRegion(xc,yc,layerReg):
             layerFaces.append(face)
    else:
      shapes=[face]
      if FClayerShape:
        edges=set()
        for w in FClayerShape.Wires:
           shapes.append(w)
           for e in w.Edges:
             shapes.append(e)
             edges.add(e)
        for e in FClayerShape.Edges:
           if e not in edges:
             shapes.append(e)
             edges.add(e)
      if len(shapes)>1:
#       pieces=shapes[0].multiFuse(shapes[1:],globalVar.fuzzyTolerance)
       pieces, map = shapes[0].generalFuse(shapes[1:], globalVar.fuzzyTolerance)          
       if pieces:
          slicedFace=pieces.Faces
       elif shapes:
          slicedFace=shapes[0].Faces
       else:
          slicedFace=[]
       layerFaces=[]
       for face in slicedFace:
         Pc=getPointInFace(face,importFac)
         xc=Pc[0]*importFac
         yc=Pc[1]*importFac
         if pointIsInLayerRegion(xc,yc,layerReg):
            layerFaces.append(face)
    layerFaces=mergeLayerFaces(layerFaces)
    return layerFaces


def create_3DSubdomain(cellName,importFac):
   subdomain_path="Subdomains/"+cellName
   import ezdxf
   import os,platform
   from operator import itemgetter
   import FreeCAD
   import Import,Part
   from BOPTools.GeneralFuseResult import GeneralFuseResult
   from . import globalVar
#   homedir = os.path.expanduser("~")
#   osType=platform.system()
#   if osType=='Windows':
#      FCuserConfigPath = homedir + "\\AppData\\FreeCAD\\user.cfg"
#   if osType=='Linux':
#      FCuserConfigPath = homedir + "/.config/FreeCAD/user.cfg"


   def addVSurf(sketch,h):
       extrude=FCdoc.addObject('PartDesign::Extrusion','Pad')
       extrude.Profile=sketch
       extrude.NewSolid=False
       extrude.Length = h
       extrude.Direction = (0, 0, 1)
       extrude.ReferenceAxis = None
       extrude.AlongSketchNormal = 0
       extrude.Type = 0
       extrude.UpToFace = None
       extrude.Reversed = False
       extrude.Offset = 0
       extrude.Visibility =True
       return extrude
   def addHSurf(sketch):
       global FCdoc
       obj=FCdoc.addObject('PartDesign::SubShapeBinder','Binder')
       obj.Support=sketch
       obj.Visibility =True
       return obj

   logger = FreeCAD.Logger('layout2fc')
   
   [cell_z0,cell_z1]=globalVar.partition_stack[cellName]
   cell_z0=float(cell_z0)
   cell_z1=float(cell_z1)

   stack_scale=1
   if 'scale' in globalVar.stack.keys():
        stack_scale=float(globalVar.stack['scale'][0])

   FCdoc=new_FCdocument(subdomain_path)
   DXFdoc=ezdxf.readfile(subdomain_path+".dxf")
   paramPath = "User parameter:BaseApp/Preferences/Mod/layoutDD"
   params = FreeCAD.ParamGet(paramPath)
   params.SetBool('groupLayers', True)
   params.SetBool('connectEdges', True)
   params.SetFloat('dxfScaling', 0.001)
   Import.readDXF(subdomain_path+".dxf", option_source=paramPath)
   FClayers = FCdoc.Objects
   partName = os.path.basename(subdomain_path)
   if not partName.startswith('CMP_'):
       partName='CMP_'+partName
   part=FCdoc.addObject("App::Part", partName)

   layer_order_and_name= []
   layerNames=set()
   for layer in DXFdoc.layers:
      lname=layer.dxf.name
      layerNames.add(lname)
      if lname not in globalVar.stack.keys():
            continue
      layer_order_and_name.append((globalVar.stack[lname][4],lname))

   for lname in globalVar.stack.keys():
       if lname not in layerNames:
          if len(globalVar.stack[lname]) >3:
              layer_order_and_name.append((globalVar.stack[lname][4],lname))

   layer_order_and_name=sorted(layer_order_and_name, key=itemgetter(0))

   FClayerShapeFromName={}
   for layer in FClayers:
      FClayerShapeFromName[layer.Name]=layer.Shape
      FCdoc.removeObject(layer.Name)
   FCclipShape = FClayerShapeFromName["ClippingPolygon"]
   if not FCclipShape.Edges:
      return

   for (lorder,lname) in layer_order_and_name:
      if lname not in globalVar.stack.keys():
            continue
      [prefix,z0i,z1i,opi,orderi]=globalVar.stack[lname]
      z0i=float(z0i)
      z1i=float(z1i)
      z0i=max(cell_z0,z0i)
      z1i=min(cell_z1,z1i)
      if z1i<z0i:
          continue
      label=prefix+"_"+lname
      pl=FreeCAD.Placement()
      pl.move(FreeCAD.Vector(0,0,z0i*stack_scale))
      label=prefix+"_"+lname
      if lname in FClayerShapeFromName.keys():
         FClayerShape=FClayerShapeFromName[lname]
         if FClayerShape.Edges:
            hasFClayerEdges=True
      else:
         FClayerShape=None
         hasFClayerEdges=False
      if opi=='vsurf':
         t=None
      elif opi=='add' or opi=='ins':
         useAllClipPoly=not hasFClayerEdges and prefix=="DIEL"
         if globalVar.mergedLayersInDXF:
           layerFaces=makeLayerFaces1(lname,FCclipShape,FClayerShape,importFac,useAllClipPoly)
         else:
           layerFaces=makeLayerFaces2(lname,FCclipShape,FClayerShape,importFac,useAllClipPoly)
         comp=None
         hvec=FreeCAD.Vector(0,0,(z1i-z0i)*stack_scale)
         for face in layerFaces:
           pad=face.extrude(hvec)
           for solid in pad.Solids:
             if comp==None:
               comp=Part.Compound(solid)
             else:
               comp.add(solid)
         if comp != None:
           layerComp=FCdoc.addObject("Part::Compound",prefix+"_"+lname)
           layerComp.Label=prefix+"_"+lname
           layerComp.Shape=comp
           layerComp.Placement=pl
           layerComp.Visibility=True
           part.addObject(layerComp)
         else:
           layerComp=None
      else:
         useAllClipPoly=not hasFClayerEdges and prefix=="WGP"
         if globalVar.mergedLayersInDXF:
           layerFaces=makeLayerFaces1(lname,FCclipShape,FClayerShape,importFac,useAllClipPoly)
         else:
           layerFaces=makeLayerFaces2(lname,FCclipShape,FClayerShape,importFac,useAllClipPoly)
         comp=None
         for face in layerFaces:
           if comp==None:
              comp=Part.Compound(face)
           else:
             comp.add(face)
         if comp != None:
           layerComp=FCdoc.addObject("Part::Compound",prefix+"_"+lname)
           layerComp.Label=prefix+"_"+lname
           layerComp.Shape=comp
           layerComp.Placement=pl
           layerComp.Visibility=True
           part.addObject(layerComp)
         else:
           layerComp=None
      if opi=='ins' or opi=='cut' and layerComp.Shape.Solids:
           if not layerComp:
                  continue
           if not layerComp.Shape.Solids:
                  continue
           for (lorderj,lnamej) in layer_order_and_name:
              if lorderj==lorder:
                 break
              [prefixj,z0j,z1j,opj,orderj2]=globalVar.stack[lnamej]
              z0j=float(z0j)
              z1j=float(z1j)
              if z0i>=z1j or z0j>=z1i:
                 continue
              objs = FCdoc.getObjectsByLabel(prefixj+"_"+lnamej)
              if not objs:
                  continue
              layerCompj=objs[0]
              tolerance=0.0
              if not layerCompj.Shape.Solids:
                  continue
              cutterTool=Part.Compound(layerComp.Shape.Solids[0])
              for isol in range(1,len(layerComp.Shape.Solids)):
                 cutterTool.add(layerComp.Shape.Solids[isol])
              rpl=FreeCAD.Placement()
              cutterTool.Placement.Base=FreeCAD.Vector(0,0,(z0i-z0j*stack_scale))
              shapes=[layerCompj.Shape,cutterTool]
              pieces, map = shapes[0].generalFuse(shapes[1:], tolerance)          
              gr =GeneralFuseResult(shapes, (pieces,map))
              slidedCompj=gr.piecesFromSource(shapes[0])
              slidedComp=gr.piecesFromSource(shapes[1])
              insertedSolids=set()
              for subcomp in slidedComp:
                for solid in subcomp.Solids:
                    insertedSolids.add(solid)
              solids=[]
              for subcomp in slidedCompj:
                for solid in subcomp.Solids:
                  if solid not in insertedSolids:
                     solids.append(solid)
              if not solids:
                 break
              comp=Part.Compound(solids[0])
              for isol in range(1,len(solids)):
                 comp.add(solids[isol])
              layerCompj.Shape=comp
   for doc in FCdoc.getDependentDocuments():
        doc.save();
   return FCdoc


def finalizeRegionDXF(layoutView,importFac,interceptedLayers,subdomain_path):
   import ezdxf
   import os
   from . import globalVar
   cellView       = layoutView.active_cellview()
   cellViewId     = cellView.index()
   cellLayout     = cellView.layout()
   cell = cellView.cell

   REGION_KEY=cell.name
   wgp_keys = [ k for k in globalVar.partition_stack.keys() if k.startswith(REGION_KEY) and len(k.split('_'))>3]
   WGNum=0
   if len(wgp_keys)>0:
        WGNum=max([int(k.split('_')[3]) for k in wgp_keys])

   layerId=[]
   layerName=[]
   layerId.append(cell.layout().layer(0,0))
   layerName.append("ClippingPolygon")
   for i in range(WGNum):
     lid =cellLayout.layer(i+1, 0)
     layerId.append(lid)
     layerName.append(f"WGP_{i+1}")

   doc=ezdxf.readfile(subdomain_path+".dxf")
   msp = doc.modelspace()
   for i in range(WGNum+1):
     if layerId[i]<0:
        continue
     points=[]
     tmp= [itr.shape().polygon.transformed(itr.trans()) for itr in cellLayout.begin_shapes(cell,layerId[i]) if itr.shape().is_polygon()]
     if tmp:
        poly=tmp[0]
        for pt in poly.each_point_hull():
           x, y = pt.x/importFac, pt.y/importFac
           points.append((x,y))
        closed=True
     else:
        tmp= [itr.shape().path.transformed(itr.trans()) for itr in cellLayout.begin_shapes(cell,layerId[i]) if itr.shape().is_path()]
        if tmp:
           path=tmp[0]
           for pt in path.each_point():
              x, y = pt.x/importFac, pt.y/importFac
              points.append((x,y))
           closed=False
     if points:
        doc.layers.add(name=layerName[i], color=7, linetype="CONTINUOUS")
        lwp = msp.add_lwpolyline(points, dxfattribs={"layer": layerName[i]})
        lwp.closed=closed

   for layername in interceptedLayers:
       if layername in globalVar.stack and not layername in doc.layers:
          doc.layers.add(name=layername)
   doc.save()



def extractSubdomainDXF(layoutView,importFac):
    from ezdxf.addons import iterdxf
    from ezdxf import bbox
    mainCellView  = layoutView.cellview(0)
    mainCellViewId = mainCellView.index()
    mainLayout     = mainCellView.layout()
    cellView       = layoutView.active_cellview()
    cellViewId     = cellView.index()
    cellLayout     = cellView.layout()
    cell = cellView.cell
    if cellViewId==mainCellViewId:
        return
    if cell is None:
       return
    mainFilePath      = mainCellView.filename()
    mainFilePathSeg   = mainFilePath.replace("\\", "/").split("/")
    mainFname         = mainFilePathSeg[-1].split(".")[0]
    cellFilePath      = cellView.active().filename()
    cellFilePathSeg   = cellFilePath.replace("\\", "/").split("/")
    cellFname         = cellFilePathSeg[-1].split(".")[0]
    mainDoc = iterdxf.opendxf(mainFname+'_flat.dxf')
    subdomain_path="Subdomains/"+cell.name
    exporter = mainDoc.export(subdomain_path+'.dxf')
    msp=mainDoc.modelspace()
    extractedTypes=["LINE","POINT","VERTEX","POLYLINE","LWPOLYLINE","SPLINE","CIRCLE","ARC","ELLIPSE"]
    cellLy00Id=cell.layout().layer(0,0)
    cellShape=cell.shapes(cellLy00Id)
    interceptedLayers=set()
    try:
      for entity in msp:
         if not entity.dxf.hasattr("layer"):
             continue
         if interceptedLayer(entity.dxf.layer,cell.name):
            interceptedLayers.add(entity.dxf.layer)
            if entity.dxftype() in extractedTypes:
              bb = bbox.extents([entity])
              ll=bb.extmin
              ur=bb.extmax
              kbb= pya.Box(ll[0]*importFac,ll[1]*importFac,ur[0]*importFac,ur[1]*importFac)
              touchPoly=[poly for poly in cellShape.each_touching(kbb)]
              if len(touchPoly)>0:
                 exporter.write(entity)
    finally:
      exporter.close()
      mainDoc.close()
      finalizeRegionDXF(layoutView,importFac,interceptedLayers,subdomain_path)


def makeSubdomain():
    from . import loaders
    layoutView        = pya.Application.instance().main_window().current_view()
    mainCellView      = layoutView.cellview(0)
    mainLayout        = mainCellView.layout()
    if mainLayout.technology() is not None:
       dxf_unit  = mainLayout.technology().load_layout_options.dxf_unit
       importFac = dxf_unit/mainLayout.dbu
    else:
       importFac=1
    cellView= layoutView.active_cellview()
    cell = cellView.cell
#    copyInterceptedLayers(layoutView)
    extractSubdomainDXF(layoutView,importFac)
    create_3DSubdomain(cell.name,importFac)


def deleteCellLayers(layoutView):
    from . import saveActiveCell
    mainCellView   = layoutView.cellview(0)
    mainCellViewId = mainCellView.index()
    cellView       = layoutView.active_cellview()
    cellViewId     = cellView.index()
    if cellViewId==mainCellViewId:
        return
    mainLayout= mainCellView.layout()
    cellLayout= cellView.layout()
    cell = cellView.cell
    for poly in clypPolygons:
        cell.shapes(cellLy00Id).insert(poly)
    for lyp in layoutView.each_layer():
       if lyp.cellview()==cellViewId:
          lid = lyp.layer_index()
          if lid<0:
             continue
          lif = cellLayout.get_info(lid)
          ln,dt = lif.layer, lif.datatype
          if ln==0:
             continue
          cell.clear(lid)
    saveActiveCell.saveActiveCell()

def deleteSubdomain():
    layoutView  = pya.Application.instance().main_window().current_view()
    deleteCellLayers(layoutView)


def create_3DSubdomFromActiveCell():
   import FreeCAD
   import Import,Part
   layoutView  = pya.Application.instance().main_window().current_view()
   mainCellView   = layoutView.cellview(0)
   mainCellViewId = mainCellView.index()
   mainLayout     = mainCellView.layout()
   cellView       = layoutView.active_cellview()
   cellViewId     = cellView.index()
   if cellViewId==mainCellViewId:
        return
   cell = cellView.cell
   if mainLayout.technology() is not None:
      dxf_unit  = mainLayout.technology().load_layout_options.dxf_unit
      importFac = dxf_unit/mainLayout.dbu
   else:
      importFac=1
   mainFilePath      = mainCellView.filename()
   mainFilePathSeg   = mainFilePath.replace("\\", "/").split("/")
   mainFname         = mainFilePathSeg[-1].split(".")[0]
   FCdoc=create_3DSubdomain(cell.name,importFac)



    
