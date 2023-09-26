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
    for lyp in layoutView.each_layer():
       if lyp.cellview()==mainCellViewId and lyp.visible:
          lid = lyp.layer_index()
          lif = mainLayout.get_info(lid)
          ln,dt = lif.layer, lif.datatype
          cell_lid = cellLayout.layer(ln, dt)
          cell_lif = cellLayout.get_info(cell_lid)
          cell_lif.name= lyp.source_name
          cellLayout.set_info(cell_lid,cell_lif)
    layoutView.add_missing_layers()
    saveActiveCell.saveActiveCell()

def makeSubdomain():
    layoutView  = pya.Application.instance().main_window().current_view()
    copyVisibleLayers(layoutView)

