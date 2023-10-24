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
    from . import loaders


    mainWindow   = pya.Application.instance().main_window()
    layoutView   = pya.Application.instance().main_window().current_view()
    cellView     = layoutView.cellview(1)
    cellViewI    = cellView.index()
    cellLayout   = cellView.layout()
    REGION_KEY="Region_1"

    partition_stack=loaders.readStack('partition.stack')
    if len(partition_stack)>0:
        REGION_KEY= "Region_"+str(1+max( [int(k.split('_')[1]) for I in partition_stack.keys()]))

    GUI_Klayout = ZextentDialog(REGION_KEY,partition_stack,pya.Application.instance().main_window())
    GUI_Klayout.exec_()

    loaders.saveStack('partition.stack',partition_stack)

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
    from . import loaders

    mainWindow   = pya.Application.instance().main_window()
    layoutView   = pya.Application.instance().main_window().current_view()
    cellView     = layoutView.cellview(1)
    cell         = cellView.cell
    cellLayout   = cellView.layout()
    REGION_KEY=cell.name

    partition_stack=loaders.readStack('partition.stack')

    GUI_Klayout = ZextentDialog(REGION_KEY,partition_stack,pya.Application.instance().main_window())
    GUI_Klayout.exec_()
#    print("Zstart : {0}".format(partition_stack[REGION_KEY][0])) 
#    print("Zend : {0}".format(partition_stack[REGION_KEY][1]))         

    loaders.saveStack('partition.stack',partition_stack)


def deleteRegion():
    import os
    from . import loaders

    mainWindow   = pya.Application.instance().main_window()
    layoutView   = pya.Application.instance().main_window().current_view()
    cellView     = layoutView.cellview(1)
    cell         = cellView.cell
    cellLayout   = cellView.layout()
    REGION_KEY=cell.name
    cellI=cell.cell_index()
    cellLayout.delete_cell(cellI)
    partition_stack=loaders.readStack('partition.stack')
    if REGION_KEY in partition_stack:
      del partition_stack[REGION_KEY]
      loaders.saveStack('partition.stack',partition_stack)


def copyVisibleLayers(layoutView):
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
    if cell is None:
       return
    cellLy00Id=cell.layout().layer(0,0)
    clypPolygons= [itr.shape().polygon.transformed(itr.trans()) for itr in cellLayout.begin_shapes(cell,cellLy00Id)]
    cell.clear(cellLy00Id)
    cellLy01Id=cell.layout().layer(0,1)
    for poly in clypPolygons:
        cell.shapes(cellLy01Id).insert(poly)
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
       if lyp.cellview()==mainCellViewId and lyp.visible:
          lif = mainLayout.get_info(lid)
          ln,dt = lif.layer, lif.datatype
          if (ln,dt)==(0,0):
             continue
          cellv_lid = cellLayout.layer(ln, dt)
          cellv_lif = cellLayout.get_info(cellv_lid)
          cellv_lif.name= lyp.source_name
          cellLayout.set_info(cellv_lid,cellv_lif)
          for poly in clypPolygons:
             cell.shapes(cellv_lid).insert(poly)
    layoutView.add_missing_layers()
    saveActiveCell.saveActiveCell()


def getCellLayerShapes(layoutView):
    mainCellView   = layoutView.cellview(0)
    mainCellViewId = mainCellView.index()
    cellView       = layoutView.active_cellview()
    cellViewId     = cellView.index()
    cellLayout= cellView.layout()
    cellLayerShapes={}
    cell =cellView.cell
    if cellViewId==mainCellViewId:
       return
    if cell is None:
       return cellLayerShapes
    for lyp in layoutView.each_layer():
       if lyp.cellview()==cellViewId:
          lid = lyp.layer_index()
          if lid<0:
             continue
          lif = cellLayout.get_info(lid)
          ln,dt = lif.layer, lif.datatype
          if ln==0:
             continue
          if cell.shapes(lid).size()==0:
              continue
          if len(lif.name)==0:
              continue
          cellLayerShapes[lif.name]=cell.shapes(lid)
    return cellLayerShapes

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


def makeLayerFaces(lname,FCclipEdges,FClayerEdges,importFac):
    import FreeCAD
    import Part
    import BOPTools.JoinAPI
    from BOPTools.GeneralFuseResult import GeneralFuseResult
    connected=BOPTools.JoinAPI.connect(FCclipEdges)
    contWire=Part.Wire(connected.Edges)
    face=Part.Face(contWire)
    if not FClayerEdges:
       layerFaces=[face]
    else:
       layerReg=evalLayerRegion(lname)
       shapes=[face]
       NcontEdges=0
       for edge in FCclipEdges:
         shapes.append(edge)
         NcontEdges=NcontEdges+1
       for edge in FClayerEdges:
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
         for edge in slicedEdge:
           slicedContour.append(edge)
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
    return layerFaces


def create_3DSubdomain(subdomain_path,stack_path,importFac):
   from . import loaders
   import ezdxf
   import os,platform
   from operator import itemgetter
   import FreeCAD
   import Import,Part
   from BOPTools.GeneralFuseResult import GeneralFuseResult
#   homedir = os.path.expanduser("~")
#   osType=platform.system()
#   if osType=='Windows':
#      FCuserConfigPath = homedir + "\\AppData\\FreeCAD\\user.cfg"
#   if osType=='Linux':
#      FCuserConfigPath = homedir + "/.config/FreeCAD/user.cfg"

   def addVSurf(sketch,h):
       global FCdoc
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
   
   stack=loaders.readStack(stack_path)
   stack_scale=1
   if 'scale' in stack.keys():
        stack_scale=float(stack['scale'][0])

   FCdoc=new_FCdocument(subdomain_path)
   DXFdoc=ezdxf.readfile(subdomain_path+".dxf")
   paramPath = "User parameter:BaseApp/Preferences/Mod/layoutDD"
   params = FreeCAD.ParamGet(paramPath)
   params.SetBool('groupLayers', True)
   params.SetBool('connectEdges', False)
   params.SetFloat('dxfScaling', 0.001)
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
   layer_order_and_name=sorted(layer_order_and_name, key=itemgetter(0))

   FClayerEdgesFromName={}
   for layer in FClayers:
      FClayerEdgesFromName[layer.Name]=layer.Shape.Edges
      FCdoc.removeObject(layer.Name)

   FCclipEdges = FClayerEdgesFromName["ClippingPolygon"]
   if not FCclipEdges:
      return

   for (lorder,lname) in layer_order_and_name:
      if lname not in stack.keys():
            continue
      [prefix,z0i,z1i,opi,orderi]=stack[lname]
      z0i=float(z0i)
      z1i=float(z1i)
      label=prefix+"_"+lname
      pl=FreeCAD.Placement()
      pl.move(FreeCAD.Vector(0,0,z0i*stack_scale))
      label=prefix+"_"+lname
      if lname in FClayerEdgesFromName.keys():
         FClayerEdges=FClayerEdgesFromName[lname]
      else:
         FClayerEdges=[]
      layerComp=FCdoc.addObject("Part::Compound",prefix+"_"+lname)
      layerComp.Label=prefix+"_"+lname
      if opi=='vsurf':
         t=None
      elif opi=='add' or opi=='ins':
         layerFaces=makeLayerFaces(lname,FCclipEdges,FClayerEdges,importFac)
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
           layerComp.Shape=comp
           layerComp.Placement=pl
           layerComp.Visibility=True
           part.addObject(layerComp)
      else:
         layerFaces=makeLayerFaces(lname,FCclipEdges,FClayerEdges,importFac)
         comp=None
         for face in layerFaces:
           if comp==None:
              comp=Part.Compound(face)
           else:
             comp.add(face)
         if comp != None:
           layerComp.Shape=comp
           layerComp.Placement=pl
           layerComp.Visibility=True
           part.addObject(layerComp)
      if opi=='ins' or opi=='cut' and layerComp.Shape.Solids:
           for (lorderj,lnamej) in layer_order_and_name:
              if lorderj==lorder:
                 break
              [prefixj,z0j,z1j,opj,orderj2]=stack[lnamej]
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


def add_clippingPolygon(poly,importFac,cellLayerShapes,subdomain_path):
   import ezdxf
   import os
   points=[]
   for pt in poly.each_point_hull():
      x, y = pt.x/importFac, pt.y/importFac
      points.append((x,y))
   doc=ezdxf.readfile(subdomain_path+".dxf")
   doc.layers.add(name="ClippingPolygon", color=7, linetype="CONTINUOUS")
   msp = doc.modelspace()
   lwp = msp.add_lwpolyline(points, dxfattribs={"layer": "ClippingPolygon"})
   lwp.closed=True
   for layername in cellLayerShapes.keys():
       if not layername in doc.layers:
          doc.layers.add(name=layername)
   doc.save()



def extractSubdomainDXF(layoutView,cellLayerShapes):
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
    if mainLayout.technology() is not None:
       dxf_unit  = mainLayout.technology().load_layout_options.dxf_unit
       importFac = dxf_unit/mainLayout.dbu
    else:
       importFac=1
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
    try:
      for entity in msp:
         if not entity.dxf.hasattr("layer"):
             continue
         if entity.dxf.layer in cellLayerShapes:
            if entity.dxftype() in extractedTypes:
              bb = bbox.extents([entity])
              ll=bb.extmin
              ur=bb.extmax
              kbb= pya.Box(ll[0]*importFac,ll[1]*importFac,ur[0]*importFac,ur[1]*importFac)
              polyShapes=cellLayerShapes[entity.dxf.layer]
              touchPoly=[poly for poly in polyShapes.each_touching(kbb)]
              if len(touchPoly)>0:
                 exporter.write(entity)
    finally:
      exporter.close()
      mainDoc.close()
      cellLy01Id=cell.layout().layer(0,1)
      clypPolygons= [itr.shape().polygon.transformed(itr.trans()) for itr in cellLayout.begin_shapes(cell,cellLy01Id)]
      add_clippingPolygon(clypPolygons[0],importFac,cellLayerShapes,subdomain_path)
      stack_path=mainFname+".stack"
      create_3DSubdomain(subdomain_path,stack_path,importFac)


def makeSubdomain():
    layoutView  = pya.Application.instance().main_window().current_view()
    copyVisibleLayers(layoutView)
    cellLayerShapes=getCellLayerShapes(layoutView)
    extractSubdomainDXF(layoutView,cellLayerShapes)

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
    cellLy01Id=cell.layout().layer(0,1)
    clypPolygons= [itr.shape().polygon.transformed(itr.trans()) for itr in cellLayout.begin_shapes(cell,cellLy01Id)]
    cell.clear(cellLy01Id)
    cellLy00Id=cell.layout().layer(0,0)
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
   stack_path=mainFname+".stack"
   subdomain_path="Subdomains/"+cell.name
   FCdoc=create_3DSubdomain(subdomain_path,stack_path,importFac)

#create_3DSubdomFromActiveCell()

    
