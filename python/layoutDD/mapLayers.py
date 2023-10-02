

import pya

def makeLayerMap(layoutView,cellView):
    itr = layoutView.begin_layers()
    layerNames=[]
    while not itr.at_end():
        lyp = itr.current()
        if lyp.cellview() == cellView.index():
            if lyp.source_layer < 0:
                layerNames.append(lyp.source_name)
        itr.next()
    layerNames.sort()
    layerMap={}
    ln=0
    dt=0
    for name in layerNames:
        ln=ln+1
        layerMap[name]=[ln, dt]
    return layerMap

def cleanLayers(layoutView,cellView):
    itr = layoutView.begin_layers()
    while not itr.at_end():
        lyp = itr.current()
        if lyp.cellview() == cellView.index():
            if (lyp.source_layer < 0):
                layoutView.delete_layer(itr)
            else:
                itr.next()

def mapLayers():
    layoutView = pya.Application.instance().main_window().current_view()
    cellView   = layoutView.active_cellview()
    layout     = cellView.layout()
    layerMap=makeLayerMap(layoutView,cellView)
    itr = layoutView.begin_layers()
    while not itr.at_end():
        lyp = itr.current()
        if lyp.cellview() == cellView.index():
            lid = lyp.layer_index()
            lnm = lyp.source_name
            if lnm in layerMap:
                lno, ldt = layerMap[lnm]
                layout.set_info(lid, pya.LayerInfo(lno, ldt, lnm))
        itr.next()
    cleanLayers(layoutView,cellView)
    layoutView.add_missing_layers()


