## Description
- `cluster_torsion_scan.ipynb`
    - Perform Kmeans clustering (n_clusters=100) using [sugar pucker pseudorotation parameters](https://pubs.acs.org/doi/10.1021/ct401013s) against diverse sugar pucker structures sampled from implicit MD.
    - Minimize clustered centroid structures with RDKit with positional restraints on sugar moeity to fix base puckering and chi bond bending arising from high temperature MD. Minimization implemented in RDKit using `MMFF94` was performed to relax and fix highly disordered atoms which will likely to cause problems for QM calculations.
    - Perform torsion scan every 15 degrees against chi dihedral atoms using RDKit.

- `openmm_structure.ipynb`
    - Perform minimization (10 steps) to relax steric clashes using `openff-2.0.0` force field.
    - Calculate relative energy and exclude high energy structures (>62.75 kcal/mol).
    - Fitlered structures are saved as `torsion_scan_x_filtered.sdf`