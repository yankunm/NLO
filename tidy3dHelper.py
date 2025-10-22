import tidy3d as td
from tidy3d import web
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path # a Python tool for working with file and folder paths safely across operating systems
from tidy3d.plugins.dispersion import FastDispersionFitter

def help():
    print("=" * 60)
    print("                TIDY3D SIMULATION STEPS            ")
    print("=" * 60)

    print(">>> INITIALIZATION <<<")
    print("0. Define wavelength or frequency range [sim_params = define_simulation_parameters(wvl_min=, wvl_max=, Nfreq=, Mesh=32, run_factor=200)]")
    print("1. Define computational domain size")
    print("2. Define grid specifications (discretization size)")
    print("3. Define structures (geometry, materials, etc.)")
    print("4. Define sources (plane wave, Gaussian beam, etc.)")
    print("5. Define monitors (fields, flux, etc.)")
    print("6. Set simulation run time")
    print("7. Specify boundary conditions\n")

    print(">>> SIMULATION <<<")
    print("• Assign simulation object (loop or single instance)")
    print("• Run simulation (locally or via cloud)\n")

    print(">>> FINALIZATION <<<")
    print("• Retrieve results")
    print("• Perform postprocessing (e.g., transmission, phase, efficiency)")
    print("• Save data to JSON/HDF5/plots\n")

    print("=" * 60)
    print("               END OF SIMULATION STEPS             ")
    print("=" * 60)


def define_simulation_parameters(wvl_min, wvl_max, Nfreq=101, Mesh=32, run_factor=200):
    """
    Define and print the basic physical setup for a Tidy3D simulation.
    Returns a dictionary with all key parameters.
    """
    fr = td.FreqRange.from_wvl_interval(wvl_min=wvl_min, wvl_max=wvl_max)
    freqs = fr.freqs(Nfreq)
    wvls = td.C_0 / freqs
    freq0 = fr.freq0
    lda0 = td.C_0 / freq0
    freqw = fr.fmax - fr.fmin
    run_time = run_factor / freqw
    # changed run time to run_factor / freqw so that the larger the bandwidth, the shorter the run time
    # this is because the wider the bandwidth, the shorter the pulse in time domain, so we don't need to run the simulation for too long
    # We just need the simulation to run long enough for the pulse to pass through the structure and reach steady state

    print("=" * 60)
    print(f"{'BASIC SIMULATION SETUP':^65}")
    print("=" * 60)
    print(f"{'[wvls] Wavelength array':<40}: {wvl_max:.4f} µm to {wvl_min:.4f} µm")
    print(f"{'[freqs] Frequency array':<40}: {fr.fmin:.4e} Hz to {fr.fmax:.4e} Hz")
    print(f"{'[Nfreq] Number of points':<40}: {Nfreq}")
    print(f"{'[freq0] Central Frequency':<40}: {freq0:.6e} Hz")
    print(f"{'[fmin]  Minimum Frequency':<40}: {fr.fmin:.6e} Hz")
    print(f"{'[fmax]  Maximum Frequency':<40}: {fr.fmax:.6e} Hz")
    print(f"{'[freqw] Bandwidth':<40}: {freqw:.6e} Hz")
    print(f"{'[lda0]  Central λ':<40}: {lda0:.6e} m")
    print(f"{'[Mesh]  Mesh cells per λ':<40}: {Mesh}")
    print(f"{'[run_time] Simulation run time':<40}: {run_time:.6e} s")
    print("=" * 60 + "\n")

    return {
        "wvls" : wvls,
        "freqs" : freqs,
        "freq0": freq0,
        "lda0": lda0,
        "freqw": freqw,
        "fmin": fr.fmin,
        "fmax": fr.fmax,
        "Mesh": Mesh,
        "run_time": run_time,
        "Nfreq": Nfreq,
    }