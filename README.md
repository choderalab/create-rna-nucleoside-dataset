Create diverse RNA nucleoside structures with high temperature implicit MD
---

### md
- Initial nucleoside structures (adenosine, cytidine, guanosine, uridine) generated using `PyMOL 2.5.1 Incentive Product (110589adb8), 2021-06-28`
    - O5' hydroxyl atom replaced with hydrogen atom to break the inner hydrogen bond between O5' hydroxyl and base group allowing better sampling of syn/anti-base conformation
- MD sampling at 500K with OBC2 implicit solvent using `openff-2.0.0` force field
    - Mulitple independent 500 ns simulations performed for each nucleside

### cluster
- Kmeans clustering performed using chi angle and [sugar pucker pseudorotation parameters](https://pubs.acs.org/doi/10.1021/ct401013s) as input features

### qca-dataset-submission-test
- Test notebook to generate input files for [QCA Dataset Submission](https://github.com/openforcefield/qca-dataset-submission)

