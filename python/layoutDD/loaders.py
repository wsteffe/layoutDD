import pya

def saveFlatDXF(fpath):
    import ezdxf
    from ezdxf import disassemble
    from ezdxf.addons import Importer
    sdoc = ezdxf.readfile(fpath+".dxf")
    tdoc = ezdxf.new()
    importer = Importer(sdoc,tdoc)
    smsp= sdoc.modelspace()
    exploded=disassemble.recursive_decompose(smsp)
    importer.import_entities(exploded)
    tdoc.saveas(fpath+"_flat.dxf")

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
    import os
    import mapLayers, saveActiveCell, globalVar
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
    filePath    = cellView.active().filename()
    filePath    = filePath.replace("\\", "/")
    globalVar.projectDir,globalVar.fileName = os.path.split(filePath)
    globalVar.fileName,fext=os.path.splitext(globalVar.fileName)
    filePath,fext  = os.path.splitext(filePath)
    stack_path=filePath+".stack"
    if not os.path.exists(stack_path):
       pya.MessageBox.info("Information", "Imported Layout must be associated with stack file", pya.MessageBox.Ok)
       return
    globalVar.stack=readStack(stack_path)
    stack_scale=1
    if 'scale' in globalVar.stack.keys():
        stack_scale=float(globalVar.stack['scale'][0])  
#    for lyp in layoutView.each_layer():
#        lyp.valid = False
    if fext.lower() == ".dxf":
      mapLayers.assignNumbersToLayers()
    if fext.lower() == ".gds":
       dxf_path=filePath+".dxf"
       if not os.path.exists(dxf_path):
          pya.MessageBox.info("Information", "Missing dxf file", pya.MessageBox.Ok)
          return
       map_path=filePath+".map"
       if not os.path.exists(map_path):
          pya.MessageBox.info("Information", "Missing ADS layer map file", pya.MessageBox.Ok)
          return
       mapLayers.assignNamesToLayers(map_path)
    saveActiveCell.saveActiveCell()
    saveFlatDXF(filePath)
    partitionPath=globalVar.projectDir+"/partition"
    subdomainsPath=globalVar.projectDir+"/Subdomains"
    if not os.path.exists(subdomainsPath):
      os.mkdir(subdomainsPath)
    if not os.path.exists(partitionPath+".gds"): 
      cellView   = mainWindow.create_layout(2)
      cellIndex  = cellView.index()
      cellLayout = cellView.layout()
      option     = pya.SaveLayoutOptions()
      layoutView = mainWindow.current_view()
      layoutView.save_as(cellIndex,partitionPath+".gds", option)
      globalVar.partition_stack={}
      saveStack(partitionPath+".stack",globalVar.partition_stack)
    else:
      layoutView.load_layout(partitionPath+".gds",2)

def openProject():
    import os
    import globalVar
    gdsPath      = pya.FileDialog.ask_open_file_name("Choose your file.", '.', "GDS2 (*.gds)")
    mainWindow   = pya.Application.instance().main_window()
    layoutView   = mainWindow.view(mainWindow.create_view())
    cellViewId   = layoutView.load_layout(gdsPath)
    cellView     = layoutView.cellview(cellViewId)
    filePath     = gdsPath.replace("\\", "/")
    globalVar.projectDir,globalVar.fileName = os.path.split(filePath) 
    globalVar.fileName,fext=os.path.splitext(globalVar.fileName)
    filePath,fext  = os.path.splitext(filePath)
    lypPath      = filePath+".lyp"
    layoutView.load_layer_props(lypPath)
    globalVar.stack=readStack(filePath+".stack")
    partitionPath=globalVar.projectDir+"/partition"
    globalVar.partition_stack=readStack(partitionPath+'.stack')
    if os.path.exists(partitionPath+".gds"):
        layoutView.load_layout(partitionPath+".gds",2)
        if os.path.exists(partitionPath+".lyp"):
           layoutView.load_layer_props(partitionPath+".lyp",cellViewId)





