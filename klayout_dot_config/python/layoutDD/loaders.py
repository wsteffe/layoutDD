import pya

def importDXF():
    import os
    from . import mapLayers, saveActiveCell
    dxfPath      = pya.FileDialog.ask_open_file_name("Choose your file.", '.', "DXF (*.dxf)")
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = mainWindow.view(mainWindow.create_view())
    option       = pya.LoadLayoutOptions()
    cellViewId   = layoutView.load_layout(dxfPath,option, 2)
    cellView     = layoutView.cellview(cellViewId)
#    for lyp in layoutView.each_layer():
#        lyp.valid = False
    mapLayers.mapLayers()
    saveActiveCell.saveActiveCell()
    if not os.path.exists("Partition"): 
        os.makedirs("Partition")

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
    if os.path.exists('Partition/MAX_REGION_INDEX'): 
        with open('Partition/MAX_REGION_INDEX','r') as f:
            MAX_REGION_INDEX=int(f.readline())
    for I in range(MAX_REGION_INDEX):
        path=f"Partition/Region_{I+1}.gds"
        if os.path.exists(path):
            layoutView.load_layout(path,2)





