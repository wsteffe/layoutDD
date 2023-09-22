import pya
mainWindow = pya.Application.instance().main_window()

def loadLayout(layoutView, path = None, lockLayers = False):
    cellViewId = layoutView.load_layout(path, 2) if path else layoutView.create_layout(2)
    cellView   = layoutView.cellview(cellViewId)
    if lockLayers:
        for lyp in layoutView.each_layer():
            lyp.valid = False
    return cellView

def importPCB():
    from . import mapLayers
    dxfPath      = r"....\KaIMUX-PCB.dxf"
    layoutView   = mainWindow.view(mainWindow.create_view())
    dxfCellView  = loadLayout(layoutView, path = dxfPath, lockLayers = True)
    mapLayers()

