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

def extractSubdomainDXF(layoutView,cellLayerShapes):
    from ezdxf.addons import iterdxf
    from ezdxf import bbox
    mainCellView  = layoutView.cellview(0)
    mainCellViewId = mainCellView.index()
    cellView       = layoutView.active_cellview()
    cellViewId     = cellView.index()
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
    mainDoc = iterdxf.opendxf(mainFname+'.dxf')
    subdom_exporter = mainDoc.export("Subdomains/"+cell.name+'.dxf')
    try:
      for entity in mainDoc.modelspace():
         if not entity.dxf.hasattr("layer"):
             continue
         if entity.dxf.layer in cellLayerShapes:
            if entity.dxftype() == 'LINE':
              bb = bbox.extents([entity])
              print(bb.extmin)
              subdom_exporter.write(entity)
            elif entity.dxftype() == 'POLYLINE':
              bb = bbox.extents([entity])
              print(bb.extmin)
              subdom_exporter.write(entity)
            if entity.dxftype() == 'CIRCLE':
              bb = bbox.extents([entity])
              print(bb.extmin)
              subdom_exporter.write(entity)
            if entity.dxftype() == 'ELLIPSE':
              subdom_exporter.write(entity)
            elif entity.dxftype() == 'TEXT':
              subdom_exporter.write(entity)
    finally:
       subdom_exporter.close()
       mainDoc.close()

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
