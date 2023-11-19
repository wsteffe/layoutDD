import pya
import os

def saveActiveCell():
    layoutView    = pya.Application.instance().main_window().current_view()
    cellView      = layoutView.active_cellview()
    layout        = cellView.layout()
    cell          = cellView.cell
    cellIndex     = cellView.index()
    filePath      = cellView.active().filename().replace("\\", "/")
    filePath,fext = os.path.splitext(filePath)
    option        = pya.SaveLayoutOptions()
    option.format = "GDS2"
    option.select_all_layers()

    if cell:
        layoutView.save_as(cellIndex,f"{filePath}.gds", option)
        layoutView.save_layer_props(f"{filePath}.lyp")


