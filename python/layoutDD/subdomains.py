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
      self.isRejected=False

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

      # double validator 
      self.dvalidator = QDoubleValidator(self)

      # creating a line edit 
      self.nameLineEdit2 = QLineEdit(self.formGroupBox)
      self.nameLineEdit2.setValidator(self.dvalidator)
      vb.addWidget(self.z2)
      vb.addWidget(self.nameLineEdit2)
      self.nameLineEdit1 = QLineEdit(self.formGroupBox)
      self.nameLineEdit1.setValidator(self.dvalidator)
      vb.addWidget(self.z1)
      vb.addWidget(self.nameLineEdit1)
      if REGION_KEY in stack:
        self.nameLineEdit1.setText(stack[REGION_KEY][0])
        self.nameLineEdit2.setText(stack[REGION_KEY][1])

      # creating a dialog button for ok and cancel 
      self.buttonBox = QDialogButtonBox(self)#.new_buttons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
      #self.buttonBox.buttonRole(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
      self.ok = self.buttonBox.addButton(QDialogButtonBox.Ok)
      self.cancel = self.buttonBox.addButton(QDialogButtonBox.Cancel)

      #(self.buttonBox.)

      # addding action when form is rejected 
      self.cancel.clicked(lambda button: self.quit())

      # adding action when form is accepted 
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
      if ',' in self.nameLineEdit1.text or ',' in self.nameLineEdit2.text:
         pya.MessageBox.info("Information", "Invalid input data", pya.MessageBox.Ok)
         return
      self.stack[self.REGION_KEY]=[self.nameLineEdit1.text,self.nameLineEdit2.text]
      # closing the window 
      self.close()

  # get info method called when form is accepted 
  def quit(self): 
      self.isRejected=True
      self.reject()

def putOnDielBoundary0(z):
    import globalVar
    t=float(z)
    for k in globalVar.stack.keys():
       if len(globalVar.stack[k]) >3:
          [prefix,z0,z1,op,order]=globalVar.stack[k]
          if float(z)<=float(z0):
             t=min(t,float(z0))
    return str(t)

def putOnDielBoundary1(z):
    import globalVar
    t=float(z)
    for k in globalVar.stack.keys():
       if len(globalVar.stack[k]) >3:
          [prefix,z0,z1,op,order]=globalVar.stack[k]
          if float(z)>=float(z1):
             t=max(t,float(z1))
    return str(t)

def newRegion():
    import os
    import saveActiveCell,loaders,globalVar

    mainWindow   = pya.Application.instance().main_window()
    layoutView   = pya.Application.instance().main_window().current_view()
    cellView     = layoutView.cellview(1)
    cellViewI    = cellView.index()
    cell         = cellView.cell
    cellLayout   = cellView.layout()

    REGI=1
    if len(globalVar.partition_stack)>0:
        REGI=1+max([int(k.split('_')[1]) for k in globalVar.partition_stack.keys()])

    REGION_KEY= "Region_"+str(REGI)
    GUI_Klayout = ZextentDialog(REGION_KEY,globalVar.partition_stack,pya.Application.instance().main_window())
    GUI_Klayout.exec_()
    if GUI_Klayout.isRejected:
        return
    globalVar.partition_stack[REGION_KEY][0]=putOnDielBoundary0(globalVar.partition_stack[REGION_KEY][0])
    globalVar.partition_stack[REGION_KEY][1]=putOnDielBoundary1(globalVar.partition_stack[REGION_KEY][1])

    partitionPath=globalVar.projectDir+"/partition"
    loaders.saveStack(partitionPath+".stack",globalVar.partition_stack)

    cellv_lid =cellLayout.layer(REGI,0)
    cellv_lif =cellLayout.get_info(cellv_lid)
    if cellv_lif.name!=REGION_KEY:
       cellv_lif.name= REGION_KEY
       cellLayout.set_info(cellv_lid,cellv_lif)
       option       = pya.SaveLayoutOptions()
       layoutView   = mainWindow.current_view()
       layoutView.add_missing_layers()
       saveActiveCell.saveActiveCell()



def name2index(name):
    I=0
    l=len(name)
    for i in range(l):
       if name[-(i+1):].isdigit():
         I=int(name[-(i+1):])
       else:
         exit
    return str(I)

def newWGP():
    import os
    import saveActiveCell,loaders,globalVar
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = mainWindow.current_view()
    cellView     = layoutView.cellview(1)
    cellViewI    = cellView.index()
    cellLayout   = cellView.layout()
    lyp=layoutView.current_layer.current()
    if lyp.cellview()!=cellViewI:
        return
    lid = lyp.layer_index()
    if lid<0:
        return
    cellv_lif = cellLayout.get_info(lid)
    REGI,dt = cellv_lif.layer, cellv_lif.datatype
    REGION_KEY= "Region_"+str(REGI)

    wgp_keys = [ k for k in globalVar.partition_stack.keys() if k.startswith(REGION_KEY) and len(k.split('_'))>3]
    WGI=1
    if len(wgp_keys)>0:
        WGI=1+max([int(k.split('_')[3]) for k in wgp_keys])
    WGP_KEY= "WGP_"+str(WGI)
    GUI_Klayout = ZextentDialog(REGION_KEY+"_"+WGP_KEY,globalVar.partition_stack,pya.Application.instance().main_window())
    GUI_Klayout.exec_()
    if GUI_Klayout.isRejected:
        return
    globalVar.partition_stack[REGION_KEY][0]=putOnDielBoundary0(globalVar.partition_stack[REGION_KEY][0])
    globalVar.partition_stack[REGION_KEY][1]=putOnDielBoundary1(globalVar.partition_stack[REGION_KEY][1])
    partitionPath=globalVar.projectDir+"/partition"
    loaders.saveStack(partitionPath+".stack",globalVar.partition_stack)
    cellv_lif =pya.LayerInfo(REGI,WGI)
    cellv_lif.name= REGION_KEY+'_'+WGP_KEY
    cellv_lid =cellLayout.layer(cellv_lif)
    option       = pya.SaveLayoutOptions()
    layoutView   = mainWindow.current_view()
    layoutView.add_missing_layers()
    saveActiveCell.saveActiveCell()


def editRegion():
    import os
    import loaders,globalVar

    mainWindow   = pya.Application.instance().main_window()
    layoutView   = pya.Application.instance().main_window().current_view()
    cellView     = layoutView.cellview(1)
    cellViewId   = cellView.index()
    cellLayout   = cellView.layout()

    lyp=layoutView.current_layer.current()
    if lyp.cellview()!=cellViewId:
        return
    lid = lyp.layer_index()
    if lid<0:
        return
    cellv_lif = cellLayout.get_info(lid)
    REGI,dt = cellv_lif.layer, cellv_lif.datatype
    REGION_KEY= "Region_"+str(REGI)

    GUI_Klayout = ZextentDialog(REGION_KEY,globalVar.partition_stack,pya.Application.instance().main_window())
    GUI_Klayout.exec_()
    if GUI_Klayout.isRejected:
        return
    globalVar.partition_stack[REGION_KEY][0]=putOnDielBoundary0(globalVar.partition_stack[REGION_KEY][0])
    globalVar.partition_stack[REGION_KEY][1]=putOnDielBoundary1(globalVar.partition_stack[REGION_KEY][1])
    loaders.saveStack(globalVar.projectDir+'/partition.stack',globalVar.partition_stack)



def editWGP():
    import os
    import saveActiveCell,loaders,globalVar
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = mainWindow.current_view()
    cellView     = layoutView.cellview(1)
    cellViewId   = cellView.index()
    cellLayout   = cellView.layout()

    lyp=layoutView.current_layer.current()
    if lyp.cellview()!=cellViewId:
        return
    lid = lyp.layer_index()
    if lid<0:
        return
    cellv_lif = cellLayout.get_info(lid)
    REGI,WGI = cellv_lif.layer, cellv_lif.datatype
    REGION_KEY= "Region_"+str(REGI)
    WGP_KEY= "WGP_"+str(WGI)
    k=REGION_KEY+"_"+WGP_KEY
    if k not in globalVar.partition_stack.keys():
        return
    GUI_Klayout = ZextentDialog(k,globalVar.partition_stack,pya.Application.instance().main_window())
    GUI_Klayout.exec_()
    if GUI_Klayout.isRejected:
        return
    globalVar.partition_stack[REGION_KEY][0]=putOnDielBoundary0(globalVar.partition_stack[REGION_KEY][0])
    globalVar.partition_stack[REGION_KEY][1]=putOnDielBoundary1(globalVar.partition_stack[REGION_KEY][1])
    loaders.saveStack(globalVar.projectDir+'/partition.stack',globalVar.partition_stack)

def deleteLayerView(layoutView,cellViewId,lid):
   it = layoutView.begin_layers()
   while not it.at_end():
       if  it.current().cellview() == cellViewId and it.current().layer_index() == lid:
           # Delete the layer
           layoutView.delete_layer(it)
       else:
           # Advance the iterator
           it.next()

def deleteWGP():
    import os
    import saveActiveCell,loaders,globalVar
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = mainWindow.current_view()
    cellView     = layoutView.cellview(1)
    cellViewId   = cellView.index()
    cell         = cellView.cell
    cellLayout   = cellView.layout()
    lyp=layoutView.current_layer.current()
    if lyp.cellview()!=cellViewId:
        return
    lid = lyp.layer_index()
    if lid<0:
        return
    cellv_lif = cellLayout.get_info(lid)
    REGI,WGI = cellv_lif.layer, cellv_lif.datatype
    REGION_KEY= "Region_"+str(REGI)
    WGP_KEY= "WGP_"+str(WGI)
    k=REGION_KEY+"_"+WGP_KEY
    if k != lyp.source_name:
        return
    if k not in globalVar.partition_stack.keys():
        return
    del globalVar.partition_stack[k]
    cell.clear(lid)
    deleteLayerView(layoutView,cellViewId,lid)
    cellLayout.delete_layer(lid)
    partitionPath=globalVar.projectDir+"/partition"
    loaders.saveStack(partitionPath+".stack",globalVar.partition_stack)
    option  = pya.SaveLayoutOptions()
    layoutView.save_as(cellViewId,partitionPath+".gds", option)
    layoutView.save_layer_props(partitionPath+".lyp")


def deleteRegion():
    import os
    import loaders, globalVar
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = pya.Application.instance().main_window().current_view()
    cellView     = layoutView.cellview(1)
    cellViewId   = cellView.index()
    cell         = cellView.cell
    cellLayout   = cellView.layout()
    lyp=layoutView.current_layer.current()
    if lyp.cellview()!=cellViewId:
        return
    lid = lyp.layer_index()
    if lid<0:
        return
    cellv_lif = cellLayout.get_info(lid)
    REGI,dt = cellv_lif.layer, cellv_lif.datatype
    k= "Region_"+str(REGI)
    if k != lyp.source_name:
        return
    if k not in globalVar.partition_stack.keys():
        return
    del globalVar.partition_stack[k]
    cell.clear(lid)
    deleteLayerView(layoutView,cellViewId,lid)
    cellLayout.delete_layer(lid)
    partitionPath=globalVar.projectDir+"/partition"
    loaders.saveStack(partitionPath+".stack",globalVar.partition_stack)
    option  = pya.SaveLayoutOptions()
    layoutView.save_as(cellViewId,partitionPath+".gds", option)
    layoutView.save_layer_props(partitionPath+".lyp")


def interceptedLayer(layerName,cellName):
    import globalVar
    if layerName not in globalVar.stack:
        return False
    if cellName not in globalVar.partition_stack:
        return False
    [prefix,z0,z1,op,order]=globalVar.stack[layerName]
    z0=float(z0)
    z1=float(z1)
    [cell_z0,cell_z1]=globalVar.partition_stack[cellName]
    cell_z0=float(cell_z0)
    cell_z1=float(cell_z1)
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
       if lyp.name!=lname and lyp.source_name!=lname:
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
       shift=3/FC_unit #3 um
       for face in slicedFace:
         Pc=getPointInFace(face,shift)
         xc=Pc[0]*FC_unit/db_unit
         yc=Pc[1]*FC_unit/db_unit
         if pointIsInLayerRegion(xc,yc,layerReg):
            layerFaces.append(face)
    layerFaces=mergeLayerFaces(layerFaces)
    return layerFaces


def create_3DSubdomain(regionName,dxf_unit,db_unit):  
   import ezdxf
   import os,platform
   from operator import itemgetter
   import FreeCAD
   import Part
   import globalVar
#   homedir = os.path.expanduser("~")
#   osType=platform.system()
#   if osType=='Windows':
#      FCuserConfigPath = homedir + "\\AppData\\FreeCAD\\user.cfg"
#   if osType=='Linux':
#      FCuserConfigPath = homedir + "/.config/FreeCAD/user.cfg"



   subdomain_path=globalVar.projectDir+"/Subdomains/"+regionName

   logger = FreeCAD.Logger('layout2fc')
   
   [cell_z0,cell_z1]=globalVar.partition_stack[regionName]
   cell_z0=float(cell_z0)
   cell_z1=float(cell_z1)

   stack=globalVar.stack

   layer_order_and_name= []
   layerNames=set()
   DXFdoc=ezdxf.readfile(subdomain_path+".dxf")
   for layer in DXFdoc.layers:
      layerNames.add(layer.dxf.name)

   l=len(regionName)
   for k in globalVar.partition_stack.keys():
      if not k.startswith(regionName) or len(k.split('_'))<=3:
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

   paramPath = "User parameter:BaseApp/Preferences/Mod/Draft"
   params = FreeCAD.ParamGet(paramPath)
   params.SetBool('groupLayers', True)
   params.SetBool('connectEdges', True)
   params.SetBool('dxfUseLegacyImporter', True)
   FC_unit=1.e3   #expressed in um
   dxfScaling=float(dxf_unit*1.e-6) #dxfScaling = dxf_unit converted in meters
   params.SetFloat('dxfScaling', dxfScaling)

   import importDXF
   inFCdoc=importDXF.open(subdomain_path+".dxf")
   for obj in inFCdoc.Objects:
      if obj.Label=="Layers":
         FClayers = obj
         break
   FClayerShapeFromName={}
   for layer in FClayers.Group:
      FClayerShapeFromName[layer.Label]=Part.Compound([obj.Shape for obj in layer.Group])
   FreeCAD.closeDocument(inFCdoc.Name)

   FCdoc=new_FCdocument(subdomain_path)
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
      if opi=='vsurf' or opi=='hsurf':
         shapeType="surf"
      elif opi=='add' or opi=='ins':
         shapeType="solid"
      else:
         shapeType="solid"
      if z1i<z0i:
          continue
      if z1i==z0i and shapeType=="solid":
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
         if not FClayerShape:
           continue
         if not FClayerShape.Edges:
           continue
         if prefix:
           layerComp=FCdoc.addObject("Part::Feature",prefix+"_"+lname)
           layerComp.Label=prefix+"_"+lname
         else:
           layerComp=FCdoc.addObject("Part::Feature",lname)
           layerComp.Label=lname
         layerComp.Visibility = True
         part.addObject(layerComp)
         contFace=Part.Face(contWire)
         edges =[e.common(contFace) for e in FClayerShape.Edges]
         surfaces=[]
         for e in edges:
            surfaces.append(e.extrude(FreeCAD.Vector(0,0,(z1i-z0i)*stack_scale)))
         layerComp.Shape=Part.Compound(surfaces)
         layerComp.Placement=layerPlacement
      elif opi=='add' or opi=='ins':
         useAllClipPoly=not hasFClayerEdges and prefix=="DIEL"
         if globalVar.mergedLayersInDXF:
           layerFaces=makeLayerFaces1(lname,FCclipShape,FClayerShape,FC_unit,db_unit,useAllClipPoly)
         else:
           layerFaces=makeLayerFaces2(lname,FCclipShape,FClayerShape,FC_unit,db_unit,useAllClipPoly)
         if not layerFaces:
           continue
         if prefix:
           layerComp=FCdoc.addObject("Part::Feature",prefix+"_"+lname)
           layerComp.Label=prefix+"_"+lname
         else:
           layerComp=FCdoc.addObject("Part::Feature",lname)
           layerComp.Label=lname
         layerComp.Visibility = True
         part.addObject(layerComp)
         solids=[]
         for f in layerFaces:
            solids.append(f.extrude(FreeCAD.Vector(0,0,(z1i-z0i)*stack_scale)))
         layerComp.Shape=Part.Compound(solids)
         layerComp.Placement=layerPlacement
         layerComp.recompute()
      elif opi=='hsurf':
         useAllClipPoly=not hasFClayerEdges
         if globalVar.mergedLayersInDXF:
           layerFaces=makeLayerFaces1(lname,FCclipShape,FClayerShape,FC_unit,db_unit,useAllClipPoly)
         else:
           layerFaces=makeLayerFaces2(lname,FCclipShape,FClayerShape,FC_unit,db_unit,useAllClipPoly)
         if not layerFaces:
           continue
         if prefix:
           layerComp=FCdoc.addObject("Part::Feature",prefix+"_"+lname)
           layerComp.Label=prefix+"_"+lname
         else:
           layerComp=FCdoc.addObject("Part::Feature",lname)
           layerComp.Label=lname
         part.addObject(layerComp)
         layerComp.Visibility = True
         surfaces=[]
         for f in layerFaces:
            surfaces.append(f)
         layerComp.Shape=Part.Compound(surfaces)
      FCdoc.recompute()
      if opi=='ins' or opi=='cut' and shapeType=="solid":
           tool=None
           objs =FCdoc.getObjectsByLabel(prefix+"_"+lname)
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
                 layerCompj=objs[0]
                 layerCompj.Shape=layerCompj.Shape.cut(tool.Shape)
           FCdoc.recompute()
   for doc in FCdoc.getDependentDocuments():
        doc.save();
   return FCdoc


def finalizeRegionDXF(layoutView,REGI,dxf_unit,interceptedLayers,subdomain_path):
   import ezdxf
   import os
   import globalVar
   cellView       = layoutView.active_cellview()
   cellViewId     = cellView.index()
   cellLayout     = cellView.layout()
   cell = cellView.cell

   dbu=cellLayout.dbu
   REGION_KEY= "Region_"+str(REGI)
   wgp_keys = [ k for k in globalVar.partition_stack.keys() if k.startswith(REGION_KEY) and len(k.split('_'))>3]
   WGNum=0
   if len(wgp_keys)>0:
        WGNum=max([int(k.split('_')[3]) for k in wgp_keys])

   layerId=[]
   layerName=[]
   layerId.append(cell.layout().layer(REGI,0))
   layerName.append("ClippingPolygon")
   for i in range(WGNum):
     lid =cellLayout.layer(REGI,i+1)
     layerId.append(lid)
     layerName.append(f"WGP_{i+1}")

   doc=ezdxf.readfile(subdomain_path+".dxf")
   msp = doc.modelspace()
   for i in range(WGNum+1):
     if layerId[i]<0:
        continue
     points=[]
     tmp= [itr.shape().polygon.transformed(itr.trans()) for itr in cellLayout.begin_shapes(cell,layerId[i]) if(itr.shape().is_polygon() or itr.shape().is_box())]
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


def extractSubdomainDXF(REGI,layoutView,dxf_unit):
    regionName= "Region_"+str(REGI)
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
    subdomain_path=globalVar.projectDir+"/Subdomains/"+regionName
    exporter = mainDoc.export(subdomain_path+'.dxf')
    msp=mainDoc.modelspace()
    extractedTypes=["LINE","POINT","VERTEX","POLYLINE","LWPOLYLINE","SPLINE","CIRCLE","ARC","ELLIPSE"]
    cellLyId=cell.layout().layer(REGI,0)
    cellShape=cell.shapes(cellLyId)
    interceptedLayers=set()
    dbu=cellLayout.dbu
    try:
      for entity in msp:
         if not entity.dxf.hasattr("layer"):
             continue
         if entity.dxftype() in extractedTypes:
            if interceptedLayer(entity.dxf.layer,regionName):
               interceptedLayers.add(entity.dxf.layer)
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
      finalizeRegionDXF(layoutView,REGI,dxf_unit,interceptedLayers,subdomain_path)


def makeSubdomain():
    import globalVar
    layoutView        = pya.Application.instance().main_window().current_view()
    mainCellView      = layoutView.cellview(0)
    mainLayout        = mainCellView.layout()
    cellView= layoutView.active_cellview()
    cellViewId= cellView.index()
    cellLayout= cellView.layout()

    lyp=layoutView.current_layer.current()
    if lyp.cellview()!=cellViewId:
        return
    lid = lyp.layer_index()
    if lid<0:
        return
    cellv_lif = cellLayout.get_info(lid)
    REGI,dt = cellv_lif.layer, cellv_lif.datatype
    REGION_KEY= "Region_"+str(REGI)
    if lyp.name!=REGION_KEY and lyp.source_name!=REGION_KEY:
        pya.MessageBox.info("Information", "Please select Subdomain Region", pya.MessageBox.Ok)
        return

    technology=cellLayout.technology()
    if cellLayout.technology() is not None:
       dxf_unit  = cellLayout.technology().load_layout_options.dxf_unit
    else:
       dxf_unit=1
    cell = cellView.cell
#    copyInterceptedLayers(layoutView)
    extractSubdomainDXF(REGI,layoutView,dxf_unit)
    create_3DSubdomain(REGION_KEY,dxf_unit,mainLayout.dbu)

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



    
