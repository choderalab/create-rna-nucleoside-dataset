#!/usr/bin/env python
# coding: utf-8
import os, sys, shutil
import pathlib
import glob as glob
import numpy as np
import warnings
import mdtraj as md
import click
import openmmtools as mmtools
from openmm.app import *
from openmm import *
from openmm.unit import *
from sys import stdout
from openmm.app import PDBFile
from pdbfixer import PDBFixer
from mdtraj.reporters import NetCDFReporter
from openff.toolkit.topology import Molecule



def export_xml(simulation, system):
    """
    Save state as XML
    """
    state = simulation.context.getState(getPositions=True, getVelocities=True, getEnergy=True, getForces=True)
    # Save and serialize the final state
    with open("state.xml", "w") as wf:
        xml = XmlSerializer.serialize(state)
        wf.write(xml)

    # Save and serialize integrator
    with open("integrator.xml", "w") as wf:
        xml = XmlSerializer.serialize(simulation.integrator)
        wf.write(xml)

    # Save the final state as a PDB
    with open("state.pdb", "w") as wf:
        PDBFile.writeFile(
            simulation.topology,
            simulation.context.getState(
                getPositions=True,
                enforcePeriodicBox=True).getPositions(),
                file=wf,
                keepIds=True
        )

    # Save and serialize system
    system.setDefaultPeriodicBoxVectors(*state.getPeriodicBoxVectors())
    with open("system.xml", "w") as wf:
        xml = XmlSerializer.serialize(system)
        wf.write(xml)


def run(**options):
    name = options["filename_noext"]
    nsteps = int(options["nsteps"])
    hmass = 3.5 * amu
    timestep = 4 * femtoseconds    
    temperature = 500 * kelvin
    checkpoint_frequency = 25000  # 100ps
    logging_frequency = 25000  # 100ps
    netcdf_frequency = 25000  # 100ps

    """
    Platform
    """
    platform = mmtools.utils.get_fastest_platform()
    platform_name = platform.getName()
    print("fastest platform is ", platform_name)
    if platform_name == "CUDA":
        # Set CUDA DeterministicForces (necessary for MBAR)
        platform.setPropertyDefaultValue('DeterministicForces', 'true')
        platform.setPropertyDefaultValue('Precision', 'mixed')
    else:
        #raise Exception("fastest platform is not CUDA")
        warnings.warn("fastest platform is not CUDA")
    
    """
    Create system
    """
    molecule = Molecule.from_file('../crd/{}.sdf'.format(name))
    from openmmforcefields.generators import SMIRNOFFTemplateGenerator
    smirnoff = SMIRNOFFTemplateGenerator(molecules=molecule, forcefield='openff-2.0.0')

    ff = ForceField('implicit/obc2.xml')
    #ff = ForceField('amber/tip3p_standard.xml')
    ff.registerTemplateGenerator(smirnoff.generator)
    
    pdbfile = PDBFile("../crd/{}.pdb".format(name))
    system = ff.createSystem(pdbfile.topology, nonbondedMethod=NoCutoff, constraints=HBonds, hydrogenMass=hmass)
    
    integrator = LangevinMiddleIntegrator(temperature, 1/picosecond, timestep)
    simulation = Simulation(pdbfile.topology, system, integrator)
    simulation.context.setPositions(pdbfile.positions)

    """
    Run
    """
    # minimize
    simulation.minimizeEnergy(maxIterations=100)    
    minpositions = simulation.context.getState(getPositions=True).getPositions()
    PDBFile.writeFile(pdbfile.topology, minpositions, open("min.pdb", 'w'))

    # define reporter
    simulation.reporters.append(NetCDFReporter('traj.nc', netcdf_frequency))
    simulation.reporters.append(CheckpointReporter('checkpoint.chk', checkpoint_frequency))
    simulation.reporters.append(StateDataReporter('reporter.log', logging_frequency, step=True, potentialEnergy=True, kineticEnergy=True, totalEnergy=True, temperature=True, speed=True))
    
    # run
    simulation.step(nsteps)

    # save
    export_xml(simulation, system)



@click.command()
@click.option('--filename_noext', required=True, help='filename without extension')
@click.option('--nsteps', default="25000", help='number of simulation steps')
def cli(**kwargs):
    run(**kwargs)



if __name__ == "__main__":
    cli()