import pya

def saveActiveCell():
    layoutView    = pya.Application.instance().main_window().current_view()
    cellView      = layoutView.active_cellview()
    layout        = cellView.layout()
    cell          = cellView.cell
    cellIndex     = cellView.index()
    filePathSeg   = cellView.active().filename().replace("\\", "/").split("/")
    path          = "/".join(filePathSeg[0:-1])
    fname          = filePathSeg[-1].split(".")[0]
    option        = pya.SaveLayoutOptions()
    option.format = "GDS2"
    option.select_all_layers()

    if cell:
        layoutView.save_as(cellIndex,f"{fname}.gds", option)
        layoutView.save_layer_props(f"{fname}.lyp")


