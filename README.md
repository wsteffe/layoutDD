
# layoutDD

This package is aimed to the Domain Decomposition of PCB circuits exported by EDA softwares.
The most used file format for the definition of a PCB sytructure is ODB++. Unfortunately an open source reader 
is not yet available for this format so I decided to import the layout geometry from dxf and gdsii files.
The Test folder included in the layoutDD project includes a dxf file, a gds file and a layer map file which are all 
generated by Keysight ADS code after having imported a circuit originally defined in the ODB++ format. 
For this purpose I have used the ODB++ circuit published at
https://www.comsol.com/model/importing-and-meshing-a-pcb-geometry-from-an-odb-archive-47681.
Thanks to the great efficiency of klayout code in dealing with large gds circuit, layoutDD may be used also in more complex cases provided that the 
extracted subdomain is limited to a reasonable size. In fact, in the company where I am employed, I have successfully tested the layoutDD
code on a very large and complex digital circuit but I am not allowd to publish these data.
The final purpose of the layoutDD project is indeed  to make it
to support the EmCAD project (see at https://github.com/wsteffe/EmCAD and http://www.hierarchical-electromagnetics.com) in the hierarchical electromagnetic 
simulation of large RF and digital PCB circuits. The basic strategy behynd layoutDD and EmCAD can be synthetized in the saying 
"*you can well eat a big elephant but only in small bite*s".


There is a redundancy in the set of data using in layoutDD import command because the geometrical shapes are described in gds file and also in the dxf file 
but the two description are nor equivalent:

* The dxf format allows a precise definition of curved shapes such as circles, ellipses, spline curves but there is a drawback. Sometimes with very complicate layouts klayout may fail to reconstruct the region covered by some layers from their dxf representation.

* The gds format offers a more reliable identification of the layer regions but all curved shapes are discretized into polygonal shapes. Another drawback is that gds format doesn't retain the layer names which are instead identified with integer indices (and an integer data types). The third file (the layer map file) exported by Keysight ADS is meant to establish a biunivocal map between these integer indices and the layer names.

The polygonal representation allows a fast implementation of several operations acting on planar shapes like union, intersection and others. The polygonal approximation is surely justified in the design of integrated circuits, which is the main application of the klayoout code. There are other applications (in example the design of RF circuits on PCBs) in which it is important to preserve a precise representation of the curved shapes. In principle a high geometrical accuracy can also be achieved trough a very fine discretization but this approach is not recommanded when the planar structure has to be imported in an electromagnetic solver based on FEM (the finite element method). In fact the fine discretization may lead to very dense tetrahedral meshes with a strong penalitization of the simulation times. It is much better to pass the exact shapes to the electromagnetic solver which may then apply an adaptive refinement process with a great improvements of the numerical efficiency.


LayoutDD package uses the gds file to identify the layer regions but it extracts the geometry inserted in a subdomain from the dxf file so that the original curved shapes are not lost.
A fourth file (the stack file) is required by layoutDD for the definition of the stackup associated with the PCB circuits.
Currently the stack file must be edited by the user which has to specify the z extent (minumum and maximum z coordinate) associated with each
dielectric and each metal layers included in the PCB structure. The format is the following:


>   layerName1: type1 Zmin1 Zmax1 operation1 oporder1

>   layerName2: type2 Zmin2 Zmax2 operation2 oporder2

>   ...

> type can be:

>     DIEL  for a dielectric layer

> 	  BC    for a metal layer or for via holes

> 	  WGP   for layer definiong waveguide ports

> oporder is the sequential order of associated operarion

> operation can be

>     add   generates a solid extrusion from Zmin to Zmax

> 	  ins   generates a solid extrusion from Zmin to Zmax which is inserted into solids generated by operations with lower order

> 	  hsurf generates an horizontal surface filling the layer region on plane z=Zmin

>     vsurf generates a surface extrusion from Zmin to Zmax


A minimal operation sequence is:

  * Create a technology using the klayout command "Tool/Manage Technology" and set the associated dxf unit for a proper reading of the dxf file. 
    This unit can be specified in the tab "Reader Options/DXF" of the created technology. Set the technology in the GUI selector.
    If the dxf unit is correct there should be a perfect fitting (same size) between the geometries described in gds and dxf files once opened in the klayout viewer. 
  * Open the gds file with the normal open command in Klayout File menu.
  * Use command Import Layout from layoutDD menu.
  * Use command New Region from layoutDD menu and fill the form with Zmin, Zmax values associated with the new subdomain.
  * Select the new region named Region_1 and the layer 0/0@2 where @2 is the tag associated with the view of partiton.gds. 
  * Draw a closed polygon on the selected layer.
  * Use the command "Make Subdomain" from the layoutDD menu.
  * The project may be closed with the normal command "File/Close All" but it should be reopened, when needed, using the command "Open DD Prject" included 
    in the layoutDD menu and then selecting, in command window, the gds file associated with the imported circuit.
  
  The layoutDD command "Make Subdomain" generates a new file named "Region_1.FCStd" inside the project subfolder named "Subdomains".
  This document contains a 3D model of the extracted geometry which can be opened with the FreeCAD software available at https://github.com/realthunder/FreeCAD/releases.
  
  The geometrical elements are all hidden once the document is opened in the FreeCAD. The visibility and a better color setting can be established with the macro
  setPCBvisibility.py (available from the subfolder python/FCmacro) invoked from the Macro menu of FC software. 
  To be recognized by FreeCAD this python script must be put inside the folder 
  "/home/username/.local/share/FreeCAD/Macro" on Linux systems and inside the folder "C:\Users\username\AppData\Roaming\FreeCAD\Macro" on Windows systems.

![Alt text](https://github.com/wsteffe/layoutDD/blob/master/Test/klayout_view.png "Imported circuit")


![Alt text](https://github.com/wsteffe/layoutDD/blob/master/Test/FC_view.png "3D model extracted from Region_1")

