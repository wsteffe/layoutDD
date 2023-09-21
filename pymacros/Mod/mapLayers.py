
mapping = { 
    "L0D0_0"     : [ 0, 0],
    "STICH-VIAS" : [10, 0],
    "BOTTOM"     : [11, 0],
    "TOP"        : [12, 0],
    "RESISTANCE" : [13, 0],
}

import pya

def mapLayers():
    global mapping
    layoutView = pya.Application.instance().main_window().current_view()
    cellView   = layoutView.active_cellview()
    layout     = cellView.layout()
    itr = layoutView.begin_layers()
    while not itr.at_end():
        lyp = itr.current()

        if lyp.cellview() == cellView.index():
            lid = lyp.layer_index()
            lnm = lyp.source_name

            if lnm in mapping:
                lno, ldt = mapping[ lnm ]
                layout.set_info(lid, pya.LayerInfo(lno, ldt, lnm))
        itr.next()
    layoutView.add_missing_layers()

def cleanLayers():
    layoutView = pya.Application.instance().main_window().current_view()
    cellView   = layoutView.active_cellview()
    itr = layoutView.begin_layers()
    while not itr.at_end():
        lyp = itr.current()
        if lyp.cellview() == cellView.index():

            if (lyp.source_layer < 0):
                layoutView.delete_layer(itr)
            else:
                itr.next()
    layoutView.add_missing_layers() 

#mapLayers()
#cleanLayers()
