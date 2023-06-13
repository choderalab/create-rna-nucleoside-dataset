## Description
- Initial nucleoside structures (adenosine, cytidine, guanosine, uridine) generated using `PyMOL 2.5.1 Incentive Product (110589adb8), 2021-06-28`.
    - O5' hydroxyl atoms were replaced with hydrogen atoms to break the inner hydrogen bond between O5' hydroxyl and base groups to improve the sampling of syn/anti conformations.
- Multiple 500 ns vanilla MD at 500K with OBC2 implicit solvent performed with `openff-2.0.0` force field using `openmm-7.7.0`.

## Usage
> cd example    
> bsub < lsf-submit-template.sh