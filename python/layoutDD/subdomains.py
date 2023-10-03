import pya

def newRegion():
    import os
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = pya.Application.instance().main_window().current_view()
    cellView     = layoutView.cellview(1)
    cellViewI    = cellView.index()
    cellLayout   = cellView.layout()
    MAX_REGION_INDEX=0
    if os.path.exists('MAX_REGION_INDEX'): 
        with open('MAX_REGION_INDEX','r') as f:
            MAX_REGION_INDEX=int(f.readline())
    with open('MAX_REGION_INDEX','w') as f:
        f.write(f'{MAX_REGION_INDEX+1}\n')
    cell         = cellLayout.create_cell(f"Region_{MAX_REGION_INDEX+1}")
    cellLayer    = cellLayout.layer(0,0)
    cellView.cell= cell
    option       = pya.SaveLayoutOptions()
    layoutView   = mainWindow.current_view()
    layoutView.add_missing_layers()
    layoutView.save_as(cellViewI,f"partition.gds", option)


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
    mainCellView  = layoutView.cellview(0)
    mainCellViewId = mainCellView.index()
    cellView       = layoutView.active_cellview()
    cellViewId     = cellView.index()
    cellLayout= cellView.layout()
    cellLayerShapes={}
    cell = cellView.cell
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


def create_3DSubdomain(subdomain_path,stack_path):
   import ezdxf
   import os
   import FreeCAD
   import Import,Part
   FCdoc=new_FCdocument(subdomain_path)
   partName = os.path.basename(subdomain_path)
   if not partName.startswith('CMP_'):
       partName='CMP_'+partName
   part=FCdoc.addObject("App::Part", partName)
   DXFdoc=ezdxf.readfile(subdomain_path+".dxf")
   paramPath = "User parameter:BaseApp/Preferences/Mod/layout2fc"
   params = FreeCAD.ParamGet(paramPath)
   params.SetBool('groupLayers', True)
   params.SetBool('connectEdges', False)
   Import.readDXF(subdomain_path+".dxf", option_source=paramPath)
   stack={}
   with open(stack_path, 'r') as f:
      for line in f:
        line=line.split('#')[0]
        [ldata,zdata]=line.split(':')
        stack[ldata]=zdata.split()
   stack_scale=1
   if 'scale' in stack.keys():
        stack_scale=float(stack['scale'][0])
   bodyName={}
   for layer in DXFdoc.layers:
      lname=layer.dxf.name
      if lname not in stack.keys():
            continue
      [prefix,z0,z1,opi,orderi]=stack[lname]
      z0=float(z0)
      z1=float(z1)
      body=FCdoc.addObject("PartDesign::Body", prefix+"_"+lname)
      bodyName[lname]=body.Name
      part.addObject(body)
      pl=FreeCAD.Placement()
      pl.move(FreeCAD.Vector(0,0,z0*stack_scale))
      body.Placement = pl
      body.Visibility = True
      body.ExportMode = 'Child Query'
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
   doc.layers.add(name="ClippingPolygon", color=7, linetype="DASHED")
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
    tech_name = "PCB"
    tech=pya.Technology.technology_by_name(tech_name)
    options=tech.load_layout_options
    importFac =options.dxf_unit/mainLayout.dbu
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
      create_3DSubdomain(subdomain_path,stack_path)


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
   cellView       = layoutView.active_cellview()
   cellViewId     = cellView.index()
   if cellViewId==mainCellViewId:
        return
   cell = cellView.cell
   subdomain_path="Subdomains/"+cell.name
   FCdoc=create_3DSubdomain(subdomain_path)
  

    
