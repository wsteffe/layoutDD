import pya

def loadLayout(layoutView, path = None, lockLayers = False):
    cellViewId = layoutView.load_layout(path, 2) if path else layoutView.create_layout(2)
    cellView   = layoutView.cellview(cellViewId)
    if lockLayers:
        for lyp in layoutView.each_layer():
            lyp.valid = False
    return cellView

def importDXF():
    from . import mapLayers, saveActiveCell
    dxfPath = pya.FileDialog.ask_open_file_name("Choose your file.", '.', "DXF (*.dxf)")
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = mainWindow.view(mainWindow.create_view())
    dxfCellView  = loadLayout(layoutView, path = dxfPath, lockLayers = True)
    mapLayers.mapLayers()
    saveActiveCell.saveActiveCell()

