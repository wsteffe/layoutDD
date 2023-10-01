import pya

def saveFlatDXF(fname):
    import ezdxf
    from ezdxf import disassemble
    doc0 = ezdxf.readfile(fname+".dxf")
    msp0=doc0.modelspace()
    doc=ezdxf.new()
    msp = doc.modelspace()
    exploded=disassemble.recursive_decompose(msp0)
    for entity in exploded:
      msp.add_entity(entity)
    doc.saveas(fname+"_flat.dxf")


def importLayout():
    import os
    from . import mapLayers, saveActiveCell
    mainWindow    = pya.Application.instance().main_window()
    layoutView    = pya.Application.instance().main_window().current_view()
    if layoutView==None:
      return
    cellView      = layoutView.active_cellview()
    filePath      = cellView.active().filename()
    filePathSeg   = filePath.replace("\\", "/").split("/")
    fname,fext    = os.path.splitext(filePathSeg[-1])
#    for lyp in layoutView.each_layer():
#        lyp.valid = False
    if fext.lower() == ".dxf":
      mapLayers.mapLayers()
      saveActiveCell.saveActiveCell()
      saveFlatDXF(fname)
    partitionPath="partition.gds"
    if not os.path.exists("Subdomains"):
      os.mkdir("Subdomains")
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
    partitionLypPath="partition.lyp"
    if os.path.exists(partitionPath):
        layoutView.load_layout(partitionPath,2)
        if os.path.exists(partitionLypPath):
           layoutView.load_layer_props(partitionLypPath,cellViewId)





