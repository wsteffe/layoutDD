import pya

def importDXF():
    from . import mapLayers, saveActiveCell
    dxfPath = pya.FileDialog.ask_open_file_name("Choose your file.", '.', "DXF (*.dxf)")
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = mainWindow.view(mainWindow.create_view())
    cellViewId   = layoutView.load_layout(dxfPath, 2)
    cellView     = layoutView.cellview(cellViewId)
#    for lyp in layoutView.each_layer():
#        lyp.valid = False
    mapLayers.mapLayers()
    saveActiveCell.saveActiveCell()

def openProject():
    gdsPath      = pya.FileDialog.ask_open_file_name("Choose your file.", '.', "GDS2 (*.gds)")
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = mainWindow.view(mainWindow.create_view())
    cellViewId   = layoutView.load_layout(gdsPath, 2)
    cellView     = layoutView.cellview(cellViewId)
    lypPath      = gdsPath.split(".")[0]+".lyp"
    layoutView.load_layer_props(lypPath)


