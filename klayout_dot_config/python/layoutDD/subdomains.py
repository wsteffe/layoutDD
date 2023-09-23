import pya

def newRegion():
    import os
    mainWindow   = pya.Application.instance().main_window()
    cellView     = mainWindow.create_layout(2)
    cellIndex    = cellView.index()
    layout       = cellView.layout()
    MAX_REGION_INDEX=0
    if os.path.exists('Partition/MAX_REGION_INDEX'): 
        with open('Partition/MAX_REGION_INDEX','r') as f:
            MAX_REGION_INDEX=int(f.readline())
    with open('Partition/MAX_REGION_INDEX','w') as f:
        f.write(f'{MAX_REGION_INDEX+1}\n')
    cell         = layout.create_cell(f"Region_{MAX_REGION_INDEX+1}")
    layoutView   = mainWindow.current_view()
    option       = pya.SaveLayoutOptions()
    layoutView.save_as(cellIndex,f"Partition/Region_{MAX_REGION_INDEX+1}.gds", option)
