
# layoutDD

This package is aimed to the Domain Decomposition of PCB layouts whuch defined in dxf files.

The dxf format allows a precise definition of curved shapes such as Circles, ellipses, spline curves.
The klayout software has the capability to import dxf files but the curvd shapes are discretized because
the internal representation is based on polygons.  

The polygonal representation allows a fast implementation of many several operations acting on planar shapes like union, intersection and others. The polygonal approximation is surely justified in the design of integrated circuits, which is the main applocation area of the klayoout code.


There are other application domains (in example the design of RF circuits on PCBs) in which it is important to preserve a precise representation of the curved shapes. In principle a high geometrical accuracy can also be achieved trough a very fine discretization but this approach is not recommanded when the planar structure has to be imported in an electromagnetic solver based on FEM (the finite element method).

In fact the fine discretization of the 2D shapes may lead to very dense tetrahedral meshes with and to a strong penalitization of the simulation times. It is much better to pass the exact curved shapes to the electromagnetic simulator which may then apply an adaptive refinement process that allows to achieve great improvements of the numerical efficiency (simulation accuracy vs simulation times).
