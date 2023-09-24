import pya

def newRegion():
    import os
    mainWindow   = pya.Application.instance().main_window()
    cellView     = mainWindow.create_layout(2)
    cellIndex    = cellView.index()
    cellLayout   = cellView.layout()
    MAX_REGION_INDEX=0
    if os.path.exists('Partition/MAX_REGION_INDEX'): 
        with open('Partition/MAX_REGION_INDEX','r') as f:
            MAX_REGION_INDEX=int(f.readline())
    with open('Partition/MAX_REGION_INDEX','w') as f:
        f.write(f'{MAX_REGION_INDEX+1}\n')
    cell         = cellLayout.create_cell(f"Region_{MAX_REGION_INDEX+1}")
    cellLayer    = cellLayout.layer(0,0)
    cellView.cell= cell
    option       = pya.SaveLayoutOptions()
    layoutView   = mainWindow.current_view()
    layoutView.add_missing_layers()
    layoutView.save_as(cellIndex,f"Partition/Region_{MAX_REGION_INDEX+1}.gds", option)
