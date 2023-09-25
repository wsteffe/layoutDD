import pya

def importDXF():
    import os
    from . import mapLayers, saveActiveCell
    dxfPath      = pya.FileDialog.ask_open_file_name("Choose your file.", '.', "DXF (*.dxf)")
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = mainWindow.view(mainWindow.create_view())
#    option       = pya.LoadLayoutOptions()
#    cellViewId   = layoutView.load_layout(dxfPath,option, 2)
    cellViewId   = layoutView.load_layout(dxfPath,"PCB")
    cellView     = layoutView.cellview(cellViewId)
#    for lyp in layoutView.each_layer():
#        lyp.valid = False
    mapLayers.mapLayers()
    saveActiveCell.saveActiveCell()
    partitionPath="partition.gds"
    if not os.path.exists(partitionPath): 
      cellView   = mainWindow.create_layout(2)
      cellIndex  = cellView.index()
      cellLayout = cellView.layout()
      option     = pya.SaveLayoutOptions()
      layoutView = mainWindow.current_view()
      layoutView.save_as(cellIndex,partitionPath, option)
      MAX_REGION_INDEX=0
      with open('MAX_REGION_INDEX','w') as f:
        f.write(f'{MAX_REGION_INDEX}\n')
    else:
      layoutView.load_layout(partitionPath,2)

def openProject():
    import os
    gdsPath      = pya.FileDialog.ask_open_file_name("Choose your file.", '.', "GDS2 (*.gds)")
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = mainWindow.view(mainWindow.create_view())
    cellViewId   = layoutView.load_layout(gdsPath, 2)
    cellView     = layoutView.cellview(cellViewId)
    lypPath      = gdsPath.split(".")[0]+".lyp"
    layoutView.load_layer_props(lypPath)
    MAX_REGION_INDEX=0
    partitionPath="partition.gds"
    if os.path.exists(partitionPath):
        layoutView.load_layout(partitionPath,2)





