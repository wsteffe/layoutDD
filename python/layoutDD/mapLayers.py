

import pya

def autoNumbersForNames(layoutView,cellView):
    itr = layoutView.begin_layers()
    layerNames=[]
    while not itr.at_end():
        lyp = itr.current()
        if lyp.cellview() == cellView.index():
            if lyp.source_layer < 0:
                layerNames.append(lyp.source_name)
        itr.next()
    layerNames.sort()
    numberForName={}
    ln=0
    dt=0
    for name in layerNames:
        ln=ln+1
        numbersForName[name]=[ln, dt]
    return numberForName


def readADSlayerMap(mapfile):
    nameForNumber={}
    with open(mapfile) as mapf:
       for line in mapf:
         line=line.split('#')[0]
         line=line.split()
         if len(line)== 4:
             name=line[0]
             ln=int(line[2])
             dt=int(line[3])
             nameForNumber[(ln,dt)]=name
    return nameForNumber
             

def cleanLayers(layoutView,cellView):
    itr = layoutView.begin_layers()
    while not itr.at_end():
        lyp = itr.current()
        if lyp.cellview() == cellView.index():
            if (lyp.source_layer < 0):
                layoutView.delete_layer(itr)
            else:
                itr.next()

def assignNumbersToLayers():
    layoutView = pya.Application.instance().main_window().current_view()
    cellView   = layoutView.active_cellview()
    layout     = cellView.layout()
    numberForName=autoNumbersForNames(layoutView,cellView)
    itr = layoutView.begin_layers()
    while not itr.at_end():
        lyp = itr.current()
        if lyp.cellview() == cellView.index():
            lid = lyp.layer_index()
            lnm = lyp.source_name
            if lnm in numberForName:
                lno, ldt = numberForName[lnm]
                layout.set_info(lid, pya.LayerInfo(lno, ldt, lnm))
        itr.next()
    cleanLayers(layoutView,cellView)
    layoutView.add_missing_layers()


def assignNamesToLayers(mapfile):
    layoutView = pya.Application.instance().main_window().current_view()
    cellView   = layoutView.active_cellview()
    layout     = cellView.layout()
    nameForNumber=readADSlayerMap(mapfile)
    itr = layoutView.begin_layers()
    while not itr.at_end():
        lyp = itr.current()
        if lyp.cellview() == cellView.index():
            lid = lyp.layer_index()
            lif = layout.get_info(lid)
            lno,ldt = lif.layer, lif.datatype
            if (lno,ldt) in nameForNumber:
                lif.name=nameForNumber[(lno,ldt)]
                layout.set_info(lid, lif)
                lyp.name=lif.name
        itr.next()
    cleanLayers(layoutView,cellView)
    layoutView.add_missing_layers()


