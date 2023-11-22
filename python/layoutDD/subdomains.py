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
      self.z1 = QLabel('Zmin')
      self.z2 = QLabel('Zmax')       

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
    import loaders,globalVar

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
    import loaders,globalVar

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

    loaders.saveStack(globalVar.projectDir+'/partition.stack',globalVar.partition_stack)


def newWGP():
    import os
    import saveActiveCell,loaders,globalVar
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
    loaders.saveStack(globalVar.projectDir+'/partition.stack',globalVar.partition_stack)
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
    import saveActiveCell,loaders,globalVar
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
    loaders.saveStack(globalVar.projectDir+'/partition.stack',globalVar.partition_stack)


def deleteWGP():
    import os
    import saveActiveCell,loaders,globalVar
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
    loaders.saveStack(globalVar.projectDir+'/partition.stack',globalVar.partition_stack)


def deleteRegion():
    import os
    import loaders, globalVar

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
      loaders.saveStack(globalVar.projectDir+'/partition.stack',globalVar.partition_stack)


def interceptedLayer(layerName,cellName):
    import globalVar
    if layerName not in globalVar.stack:
        return False
    if cellName not in globalVar.partition_stack:
        return False
    [prefix,z0,z1,op,order]=globalVar.stack[layerName]
    [cell_z0,cell_z1]=globalVar.partition_stack[cellName]
    return z0<=cell_z1 and z1>=cell_z0


def copyInterceptedLayers(layoutView):
    import saveActiveCell, globalVar
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
       if not lyp.name:
           continue
       if lyp.cellview()==cellViewId and lyp.visible:
          cellv_lif = cellLayout.get_info(lid)
          ln,dt = cellv_lif.layer, cellv_lif.datatype
          if (ln,dt)==(0,1):
             lyp.visible=False
       if lyp.cellview()==mainCellViewId:
          if lyp.name not in globalVar.stack:
            continue
          [prefix,z0,z1,op,order]=globalVar.stack[lyp.name]
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
          cellv_lif.name= lyp.name
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
       if lyp.name!=lname:
           continue
       layerReg =pya.Region([itr.shape().polygon.transformed(itr.trans()) for itr in mainLayout.begin_shapes(mainCell, lid)])
   return layerReg

def pointIsInLayerRegion(x,y,layerReg):
   if not layerReg:
      return False
   box = pya.Box(x-1, y-1, x+1, y+1)
   region_b = pya.Region(box)
   result = layerReg.interacting(region_b)
   if not result.is_empty():
      return True
   else:
      return False

def getPointInFace(face,shift):
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
           return p+sgn*bn*shift
    if eddgeMinR:
        t = eddgeMinR.Curve.tangent((eddgeMinR.ParameterRange[0]+eddgeMinR.ParameterRange[1])/2)[0]
        p = eddgeMinR.Curve.value((eddgeMinR.ParameterRange[0]+eddgeMinR.ParameterRange[1])/2)
        bn=n.cross(t)
        return p+sgn*bn*shift
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


def makeLayerFaces1(lname,FCclipShape,FClayerShape,FC_unit,db_unit,useAllClipPoly=False):
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
       xc=Pc[0]*FC_unit/db_unit
       yc=Pc[1]*FC_unit/db_unit
       layerFaces=[]
       if layerReg:
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
          xc=Pc[0]*FC_unit/db_unit
          yc=Pc[1]*FC_unit/db_unit
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


def makeLayerFaces2(lname,FCclipShape,FClayerShape,FC_unit,db_unit,useAllClipPoly=False):
    import FreeCAD
    import Part
    from BOPTools.GeneralFuseResult import GeneralFuseResult
    import globalVar
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
       xc=Pc[0]*FC_unit/db_unit
       yc=Pc[1]*FC_unit/db_unit
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
       shift=2/FC_unit #2 um
       for face in slicedFace:
         Pc=getPointInFace(face,shift)
         xc=Pc[0]*FC_unit/db_unit
         yc=Pc[1]*FC_unit/db_unit
         if pointIsInLayerRegion(xc,yc,layerReg):
            layerFaces.append(face)
    layerFaces=mergeLayerFaces(layerFaces)
    return layerFaces

useBooleanFeature=True

def create_3DSubdomain(cellName,dxf_unit,db_unit):  
   import ezdxf
   import os,platform
   from operator import itemgetter
   import FreeCAD
   import Import,Part
   from BOPTools.GeneralFuseResult import GeneralFuseResult
   import globalVar
#   homedir = os.path.expanduser("~")
#   osType=platform.system()
#   if osType=='Windows':
#      FCuserConfigPath = homedir + "\\AppData\\FreeCAD\\user.cfg"
#   if osType=='Linux':
#      FCuserConfigPath = homedir + "/.config/FreeCAD/user.cfg"


   def addPad(doc,profile,h):
       obj=doc.addObject('PartDesign::Pad','Pad')
       obj.Profile=profile
       obj.NewSolid=True
       obj.Length = h
       obj.Direction = (0, 0, 1)
       obj.ReferenceAxis = None
       obj.AlongSketchNormal = 0
       obj.Type = 0
       obj.UpToFace = None
       obj.Reversed = False
       obj.Offset = 0
       obj.Visibility =True
       obj.addProperty('App::PropertyBool', 'Group_EnableExport', 'Group')
       obj.Group_EnableExport = True
       return obj

   def addPocket(doc,profile,h):
       obj=doc.addObject('PartDesign::Pocket','Pocket')
       obj.Profile=profile
       obj.Length = h
       obj.Reversed = True
       obj.Visibility =True
       obj.addProperty('App::PropertyBool', 'Group_EnableExport', 'Group')
       obj.Group_EnableExport = True
       return obj

   def addVSurf(doc,profile,h):
       obj=doc.addObject('PartDesign::Extrusion','Extr')
       obj.Profile=profile
       obj.NewSolid=False
       obj.Length = h
       obj.Direction = (0, 0, 1)
       obj.ReferenceAxis = None
       obj.AlongSketchNormal = 0
       obj.Type = 0
       obj.UpToFace = None
       obj.Reversed = False
       obj.Offset = 0
       obj.Visibility =True
       obj.addProperty('App::PropertyBool', 'Group_EnableExport', 'Group')
       obj.Group_EnableExport = True
       return obj

   def addHSurf(doc,profile):
       obj=FCdoc.addObject('PartDesign::SubShapeBinder','Binder')
       obj.Support=profile
       obj.Visibility =True
       obj.addProperty('App::PropertyBool', 'Group_EnableExport', 'Group')
       obj.Group_EnableExport = True
       return obj

   subdomain_path=globalVar.projectDir+"/Subdomains/"+cellName

   logger = FreeCAD.Logger('layout2fc')
   
   [cell_z0,cell_z1]=globalVar.partition_stack[cellName]
   cell_z0=float(cell_z0)
   cell_z1=float(cell_z1)

   stack=globalVar.stack

   layer_order_and_name= []
   layerNames=set()
   DXFdoc=ezdxf.readfile(subdomain_path+".dxf")
   for layer in DXFdoc.layers:
      layerNames.add(layer.dxf.name)

   l=len(cellName)
   for k in globalVar.partition_stack.keys():
      if not k.startswith(cellName) or len(k.split('_'))<=3:
         continue
      lname=k[l+1:]
      if lname not in stack.keys() and lname in layerNames and lname.startswith("WGP_"):
         op=None
         if globalVar.partition_stack[k][0]==globalVar.partition_stack[k][1]:
            op="hsurf"
         elif globalVar.partition_stack[k][0]<globalVar.partition_stack[k][1]:
            op="vsurf"
         if op:
            lorder="0"
            stack[lname]=[None, globalVar.partition_stack[k][0],globalVar.partition_stack[k][1], op, lorder]

   stack_scale=1
   if 'scale' in stack.keys():
        stack_scale=float(stack['scale'][0])

   FCdoc=new_FCdocument(subdomain_path)
   paramPath = "User parameter:BaseApp/Preferences/Mod/layoutDD"
   params = FreeCAD.ParamGet(paramPath)
   params.SetBool('groupLayers', True)
   params.SetBool('connectEdges', True)
   FC_unit=1.e3   #expressed in um
   dxfScaling=float(dxf_unit*1.e-6) #dxfScaling = dxf_unit converted in meters
   params.SetFloat('dxfScaling', dxfScaling)
   Import.readDXF(subdomain_path+".dxf", option_source=paramPath)
   FClayers = FCdoc.Objects
   partName = os.path.basename(subdomain_path)
   if not partName.startswith('CMP_'):
       partName='CMP_'+partName
   part=FCdoc.addObject("App::Part", partName)

   layer_order_and_name= []
   for layer in DXFdoc.layers:
      lname=layer.dxf.name
      if lname not in stack.keys():
            continue
      layer_order_and_name.append((stack[lname][4],lname))

   for lname in stack.keys():
       if lname not in layerNames:
          if len(stack[lname]) >3:
              layer_order_and_name.append((stack[lname][4],lname))

   layer_order_and_name=sorted(layer_order_and_name, key=itemgetter(0))

   FClayerShapeFromName={}
   for layer in FClayers:
      FClayerShapeFromName[layer.Name]=layer.Shape
      FCdoc.removeObject(layer.Name)
   FCclipShape = FClayerShapeFromName["ClippingPolygon"]
   if not FCclipShape.Edges:
      return

   for (lorder,lname) in layer_order_and_name:
      if lname not in stack.keys():
            continue
      [prefix,z0i,z1i,opi,orderi]=stack[lname]
      z0i=float(z0i)
      z1i=float(z1i)
      z0i=max(cell_z0,z0i)
      z1i=min(cell_z1,z1i)
      if z1i<z0i:
          continue
      if prefix:
         label=prefix+"_"+lname
      else:
         label=lname
      layerPlacement=FreeCAD.Placement()
      layerPlacement.move(FreeCAD.Vector(0,0,z0i*stack_scale))
      if lname in FClayerShapeFromName.keys():
         FClayerShape=FClayerShapeFromName[lname]
         if FClayerShape.Edges:
            hasFClayerEdges=True
      else:
         FClayerShape=None
         hasFClayerEdges=False
      comp=None
      if opi=='vsurf':
         contWire=Part.Wire(FCclipShape.Edges)
         if not FClayerShape.Edges:
           continue
         if prefix:
           layerBody=FCdoc.addObject("PartDesign::Body",prefix+"_"+lname)
           layerBody.Label=prefix+"_"+lname
         else:
           layerBody=FCdoc.addObject("PartDesign::Body",lname)
           layerBody.Label=lname
         layerBody.Visibility = True
         layerBody.ExportMode = 'Child Query'
         part.addObject(layerBody)
         face=Part.Face(contWire)
         i=0
         edges=FCdoc.addObject('PartDesign::Feature', f'{lname}_edges')
         edges.Label = f'{lname}_edges'
         edges.Shape = Part.Compound([e.common(face) for e in FClayerShape.Edges])
         edges.Placement=layerPlacement
         edges.recompute()
         layerBody.addObject(edges)
         extr=addVSurf(FCdoc,edges,(z1i-z0i)*stack_scale)
         extr.Label = f'{lname}_surf'
         layerBody.addObject(extr)
      elif opi=='add' or opi=='ins':
         useAllClipPoly=not hasFClayerEdges and prefix=="DIEL"
         if globalVar.mergedLayersInDXF:
           layerFaces=makeLayerFaces1(lname,FCclipShape,FClayerShape,FC_unit,db_unit,useAllClipPoly)
         else:
           layerFaces=makeLayerFaces2(lname,FCclipShape,FClayerShape,FC_unit,db_unit,useAllClipPoly)
         if not layerFaces:
           continue
         if prefix:
           layerBody=FCdoc.addObject("PartDesign::Body",prefix+"_"+lname)
           layerBody.Label=prefix+"_"+lname
         else:
           layerBody=FCdoc.addObject("App::Part",lname)
           layerBody.Label=lname
         layerBody.Visibility = True
         layerBody.ExportMode = 'Child Query'
         part.addObject(layerBody)
         fwires=[]
         for f in layerFaces:
            for w in f.Wires:
               fwires.append(w)
         wires=FCdoc.addObject('PartDesign::Feature', f'{lname}_wires')
         wires.Label = f'{lname}_wires'
         wires.Shape=Part.Compound(fwires)
         wires.Placement=layerPlacement
         wires.recompute()
         layerBody.addObject(wires)
         pad=addPad(FCdoc,wires,(z1i-z0i)*stack_scale)
         pad.Label = f'{lname}_solid'
         layerBody.addObject(pad)
      else:
         useAllClipPoly=not hasFClayerEdges
         if globalVar.mergedLayersInDXF:
           layerFaces=makeLayerFaces1(lname,FCclipShape,FClayerShape,FC_unit,db_unit,useAllClipPoly)
         else:
           layerFaces=makeLayerFaces2(lname,FCclipShape,FClayerShape,FC_unit,db_unit,useAllClipPoly)
         if not layerFaces:
           continue
         if prefix:
           layerBody=FCdoc.addObject("PartDesign::Body",prefix+"_"+lname)
           layerBody.Label=prefix+"_"+lname
         else:
           layerBody=FCdoc.addObject("App::Part",lname)
           layerBody.Label=lname
         layerBody.Visibility = True
         layerBody.ExportMode = 'Child Query'
         part.addObject(layerBody)
         fwires=[]
         for f in layerFaces:
            for w in f.Wires:
               fwires.append(w)
         wires=FCdoc.addObject('PartDesign::Feature', f'{lname}_wires')
         wires.Label = f'{lname}_wires'
         wires.Shape=Part.Compound(fwires)
         wires.Placement=layerPlacement
         wires.recompute()
         layerBody.addObject(wires)
         surf=addHSurf(FCdoc,wires)
         surf.Label = f'{lname}_surf'
         layerBody.addObject(surf)
      if opi=='vsurf' or opi=='hsurf':
         shapeType="surf"
      elif opi=='add' or opi=='ins':
         shapeType="solid"
      else:
         shapeType="solid"
      FCdoc.recompute()
      if opi=='ins' or opi=='cut' and shapeType=="solid":
           tool=None
           if useBooleanFeature:
              objs =FCdoc.getObjectsByLabel(lname+"_solid")
              if objs:
                  tool=objs[0]
           for (lorderj,lnamej) in layer_order_and_name:
              if lorderj==lorder:
                 break
              [prefixj,z0j,z1j,opj,orderj2]=stack[lnamej]
              if opj=='add' or opj=='ins':
                 z0j=float(z0j)
                 z1j=float(z1j)
                 if z0i>=z1j or z0j>=z1i:
                   continue
                 if prefixj:
                   objs =FCdoc.getObjectsByLabel(prefixj+"_"+lnamej)
                 else:
                   objs =FCdoc.getObjectsByLabel(lnamej)
                 if not objs:
                   continue
                 layerBodyj=objs[0]
                 if opj=='vsurf' or opj=='hsurf':
                    shapeTypej="surf"
                 elif opj=='add' or opj=='ins':
                    shapeTypej="solid"
                 else:
                    continue
                 cutted=layerBodyj.Tip
                 cutted.Group_EnableExport = False
                 if useBooleanFeature:
                    cuttedRef=FCdoc.addObject('PartDesign::SubShapeBinder','ShepeBinder')
                    cuttedRef.Support=cutted
                    cuttedRef.Label="Reference("+cutted.Label+")"
                    layerBodyj.addObject(cuttedRef)
                    toolRef=FCdoc.addObject('PartDesign::SubShapeBinder','ShepeBinder')
                    toolRef.Support=tool
                    toolRef.Label="Reference("+tool.Label+")"
                    layerBodyj.addObject(toolRef)
                    booleanCut=FCdoc.addObject('PartDesign::Boolean','BooleanCut')
                    booleanCut.Type =1
                    booleanCut.Label=lnamej+"_cut"
                    booleanCut.setObjects([cuttedRef,toolRef])
                    booleanCut.addProperty('App::PropertyBool', 'Group_EnableExport', 'Group')
                    booleanCut.Group_EnableExport = True
                    layerBodyj.addObject(booleanCut)
                 else:
                    pocket=addPocket(FCdoc,wires1,(z1i-z0i)*stack_scale)
                    pocket.Label="Pocket_"+lnamej+"_"+lname
                    layerBodyj.addObject(pocket)
           FCdoc.recompute()
   for doc in FCdoc.getDependentDocuments():
        doc.save();
   return FCdoc


def finalizeRegionDXF(layoutView,dxf_unit,interceptedLayers,subdomain_path):
   import ezdxf
   import os
   import globalVar
   cellView       = layoutView.active_cellview()
   cellViewId     = cellView.index()
   cellLayout     = cellView.layout()
   cell = cellView.cell

   dbu=cellLayout.dbu
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
           x, y = pt.x*dbu/dxf_unit, pt.y*dbu/dxf_unit
           points.append((x,y))
        closed=True
     else:
        tmp= [itr.shape().path.transformed(itr.trans()) for itr in cellLayout.begin_shapes(cell,layerId[i]) if itr.shape().is_path()]
        if tmp:
           path=tmp[0]
           for pt in path.each_point():
              x, y = pt.x*dbu/dxf_unit, pt.y*dbu/dxf_unit
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


def extractSubdomainDXF(cellName,layoutView,dxf_unit):
    from ezdxf.addons import iterdxf
    from ezdxf import bbox
    import globalVar
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
    cellFilePath      = cellView.active().filename()
    cellFilePathSeg   = cellFilePath.replace("\\", "/").split("/")
    cellFname         = cellFilePathSeg[-1].split(".")[0]
    mainDoc = iterdxf.opendxf(globalVar.projectDir+"/"+globalVar.fileName+'_flat.dxf')
    subdomain_path=globalVar.projectDir+"/Subdomains/"+cellName
    exporter = mainDoc.export(subdomain_path+'.dxf')
    msp=mainDoc.modelspace()
    extractedTypes=["LINE","POINT","VERTEX","POLYLINE","LWPOLYLINE","SPLINE","CIRCLE","ARC","ELLIPSE"]
    cellLy00Id=cell.layout().layer(0,0)
    cellShape=cell.shapes(cellLy00Id)
    interceptedLayers=set()
    dbu=cellLayout.dbu
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
              kbb= pya.Box(ll[0]*dxf_unit/dbu,ll[1]*dxf_unit/dbu,ur[0]*dxf_unit/dbu,ur[1]*dxf_unit/dbu)
              touchPoly=[poly for poly in cellShape.each_touching(kbb)]
              if len(touchPoly)>0:
                 exporter.write(entity)
    finally:
      exporter.close()
      mainDoc.close()
      finalizeRegionDXF(layoutView,dxf_unit,interceptedLayers,subdomain_path)


def makeSubdomain():
    import globalVar
    layoutView        = pya.Application.instance().main_window().current_view()
    mainCellView      = layoutView.cellview(0)
    mainLayout        = mainCellView.layout()
    cellView= layoutView.active_cellview()
    cellLayout= cellView.layout()
    technology=cellLayout.technology()
    if cellLayout.technology() is not None:
       dxf_unit  = cellLayout.technology().load_layout_options.dxf_unit
    else:
       dxf_unit=1
    cell = cellView.cell
#    copyInterceptedLayers(layoutView)
    if not cell.name.startswith("Region"):
       pya.MessageBox.info("Information", "Please select Subdomain Region", pya.MessageBox.Ok)
       return
    extractSubdomainDXF(cell.name,layoutView,dxf_unit)
    create_3DSubdomain(cell.name,dxf_unit,mainLayout.dbu)

def makeSubdomain2():
    import globalVar
    layoutView        = pya.Application.instance().main_window().current_view()
    mainCellView      = layoutView.cellview(0)
    mainLayout        = mainCellView.layout()
    if mainLayout.technology() is not None:
       dxf_unit  = mainLayout.technology().load_layout_options.dxf_unit
    else:
       dxf_unit=1
    cellView= layoutView.active_cellview()
    cell = cellView.cell
    if not cell.name.startswith("Region"):
       pya.MessageBox.info("Information", "Please select Subdomain Region", pya.MessageBox.Ok)
    create_3DSubdomain(cell.name,dxf_unit,mainLayout.dbu)



def deleteCellLayers(layoutView):
    import saveActiveCell
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



    
