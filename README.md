Create diverse RNA nucleoside structures for QCA Dataset Submission
---

./md
- Initial nucleoside structures (adenosine, cytidine, guanosine, uridine) generated using `PyMOL 2.5.1 Incentive Product (110589adb8), 2021-06-28`.
    - O5' hydroxyl atom replaced with hydrogen atom to break the inner hydrogen bond between O5' hydroxyl and base group allowing better sampling of syn/anti-base conformation.
- Multiple 500 ns MD at 500K with OBC2 implicit solvent using `openff-2.0.0` force field.

./analysis
- cluster_torsion_scan.ipynb
    - Perform Kmeans clustering (n_clusters=100) using [sugar pucker pseudorotation parameters](https://pubs.acs.org/doi/10.1021/ct401013s) against diverse sugar pucker structures sampled from implicit MD.
    - Minimize clustered centroid structures with RDKit with positional restraints on sugar moeity to fix base puckering and chi bond bending arising from high temperature MD. `MMFF94` force field provided by RDKit is used for minimiaztion. Note that minimization is not intended to perfectly fix the weird structures but to relax and fix highly disordered atoms which will likely to cause problems for QM calculations.
    - Perform torsion scan every 15 degrees against chi dihedral atoms using RDKit.
- filter_structure.ipynb
    - Perform minimization (10 steps) to relax steric clashes using `openff-2.0.0` force field.
    - Calculate relative energy and exclude high energy structures (>62.75 kcal/mol).

./qca-dataset-submission-test
- Test notebook for [QCA Dataset Submission](https://github.com/openforcefield/qca-dataset-submission).

