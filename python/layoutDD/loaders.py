import pya

def saveFlatDXF(fname):
    import ezdxf
    from ezdxf import disassemble
    from ezdxf.addons import Importer
    sdoc = ezdxf.readfile(fname+".dxf")
    tdoc = ezdxf.new()
    importer = Importer(sdoc,tdoc)
    smsp= sdoc.modelspace()
    exploded=disassemble.recursive_decompose(smsp)
    importer.import_entities(exploded)
    tdoc.saveas(fname+"_flat.dxf")


def saveStack(stack_path,stack):
    with open(stack_path, 'w') as f:
       for I in stack.keys():
          f.write(I+":")
          for j in range(len(stack[I])):
             f.write("  "+stack[I][j])
          f.write('\n')


def readStack(stack_path):
    import os
    stack={}
    if os.path.exists(stack_path):
      with open(stack_path, 'r') as f:
        for line in f:
          if len(line.strip()) > 0:
            line=line.split('#')[0]
            [ldata,zdata]=line.split(':')
            stack[ldata]=zdata.split()
    return stack

def mergeLayers(mainLayout):
    for li in mainLayout.layer_indexes():
        topcell=mainLayout.top_cell()
        region=pya.Region(topcell.begin_shapes_rec(li))
        region.merge()
        topcell.layout().clear_layer(li)
        topcell.shapes(li).insert(region)

def importLayout():
    global layerMap
    import os
    from . import mapLayers, saveActiveCell
    mainWindow    = pya.Application.instance().main_window()
    layoutView    = pya.Application.instance().main_window().current_view()
    if layoutView==None:
      return
    cellView      = layoutView.active_cellview()
    mainLayout    = cellView.layout()
#    mergeLayers(mainLayout)
    if mainLayout.technology() is None:
      pya.MessageBox.info("Information", "Imported Layout must be associated with a Technology", pya.MessageBox.Ok)
      return
    filePath      = cellView.active().filename()
    filePathSeg   = filePath.replace("\\", "/").split("/")
    fname,fext    = os.path.splitext(filePathSeg[-1])
    stack_path=fname+".stack"
    if not os.path.exists(stack_path):
       pya.MessageBox.info("Information", "Imported Layout must be associated with stack file", pya.MessageBox.Ok)
       return
    stack=readStack(stack_path)
    stack_scale=1
    if 'scale' in stack.keys():
        stack_scale=float(stack['scale'][0])  
#    for lyp in layoutView.each_layer():
#        lyp.valid = False
    if fext.lower() == ".dxf":
      layerMap=mapLayers.mapLayers(stack)
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
      partition_stack={}
      saveStack('partition.stack',partition_stack)
    else:
      layoutView.load_layout(partitionPath,2)

def openProject():
    import os
    gdsPath      = pya.FileDialog.ask_open_file_name("Choose your file.", '.', "GDS2 (*.gds)")
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = mainWindow.view(mainWindow.create_view())
    cellViewId   = layoutView.load_layout(gdsPath)
    cellView     = layoutView.cellview(cellViewId)
    lypPath      = gdsPath.split(".")[0]+".lyp"
    layoutView.load_layer_props(lypPath)
    partitionPath="partition.gds"
    partitionLypPath="partition.lyp"
    if os.path.exists(partitionPath):
        layoutView.load_layout(partitionPath,2)
        if os.path.exists(partitionLypPath):
           layoutView.load_layer_props(partitionLypPath,cellViewId)





