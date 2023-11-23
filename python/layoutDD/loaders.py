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
    mainCellView  = layoutView.active_cellview()
    mainLayout    = mainCellView.layout()
#    mergeLayers(mainLayout)
    if mainLayout.technology() is None:
      pya.MessageBox.info("Information", "Imported Layout must be associated with a Technology", pya.MessageBox.Ok)
      return
    filePath    = mainCellView.active().filename()
    filePath    = filePath.replace("\\", "/")
    globalVar.projectDir,globalVar.fileName = os.path.split(filePath)
    globalVar.fileName,fext=os.path.splitext(globalVar.fileName)
    filePath,fext  = os.path.splitext(filePath)
    mainLayout.technology().save(filePath+".lyt")
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
      techName   = mainLayout.technology_name
      cellView   = mainWindow.create_layout(techName,2)
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
    gdsPath      = gdsPath.replace("\\", "/")
    filePath,fext  =os.path.splitext(gdsPath)
    globalVar.projectDir,globalVar.fileName = os.path.split(filePath) 
    globalVar.stack=readStack(filePath+".stack")
    mainWindow =pya.Application.instance().main_window()
    technology =pya.Technology()
    technology.load(filePath+".lyt")
    if not pya.Technology().has_technology(technology.name):
       technology=pya.Technology().create_technology(technology.name)
       technology.load(filePath+".lyt")
    mainCellView  = mainWindow.load_layout(gdsPath,technology.name,1)
    mainLayout    = mainCellView.layout()
    dxf_unit      = mainLayout.technology().load_layout_options.dxf_unit
    lypPath= filePath+".lyp"
    layoutView  = pya.LayoutView.current()
    layoutView.load_layer_props(lypPath)
    partitionPath=globalVar.projectDir+"/partition"
    globalVar.partition_stack=readStack(partitionPath+'.stack')
    if os.path.exists(partitionPath+".gds"):
        cellViewId=layoutView.load_layout(partitionPath+".gds",technology.name,2)
        cellView = layoutView.cellview(cellViewId)
        cellLayout= cellView.layout()
        if os.path.exists(partitionPath+".lyp"):
           cellView.load_layer_props(partitionPath+".lyp",cellViewId)





