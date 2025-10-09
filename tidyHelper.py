import numpy as np
import tidy3d as td

def wvl_range(wvl_min, wvl_max, N):
    fr = td.FreqRange.from_wvl_interval(wvl_min=wvl_min, wvl_max=wvl_max)
    N=N
    freqs=fr.freqs(N)
    freq0 = fr.freq0
    lda0 = td.C_0 / fr.freq0
    fwidth = fr.fmax - fr.fmin
    return freqs, freq0, lda0, fwidth

def domain_size(structure_height, substrate_height, periodicity):
    h = structure_height  # Height of cylinder
    spc = substrate_height + 3
    Lz = spc + h + spc + h
    P = periodicity # periodicity
    sim_size = [P, P, Lz]
    return sim_size

def autoGrid(periodicity, min_steps_per_wvl=32):
    dl = periodicity / min_steps_per_wvl
    horizontal_grid = td.UniformGrid(dl=dl)
    vertical_grid = td.AutoGrid(min_steps_per_wvl=32)
    grid_spec=td.GridSpec(
        grid_x=horizontal_grid,
        grid_y=horizontal_grid,
        grid_z=vertical_grid,
    )
    return grid_spec

def start_simulation(wvl_range, structure_height, substrate_height, periodicity, min_steps_per_wvl=32):
    return 


def gaussian_cp(freq0, fwidth, size, center, direction, pol):
    # define a plane wave polarized in the x direction
    plane_wave_x = td.PlaneWave(
        source_time=td.GaussianPulse(freq0=freq0, fwidth=fwidth, phase=phase),
        size=size,
        center=center,
        direction=direction,
        pol_angle=0,
    )

    # determine the phase difference given the polarization
    if pol == "l" or "L":
        phase = -np.pi / 2
    elif pol == "r" or "R":
        phase = np.pi / 2
    else:
        raise ValueError("pol must be `lcp` or `rcp`")

    # define a plane wave polarized in the y direction with a phase difference
    plane_wave_y = td.PlaneWave(
        source_time=td.GaussianPulse(freq0=freq0, fwidth=fwidth, phase=phase),
        size=size,
        center=center,
        direction=direction,
        pol_angle=np.pi / 2,
    )

    return [plane_wave_x, plane_wave_y]

def monitor(center, size, freqs, normal_dir):
    return td.DiffractionMonitor(
        center=center,
        size=size,
        freqs=freqs,
        name='diffraction_monitor',
        normal_dir=normal_dir, # away from structure
    )

def conveff(sim_data, input_pol=None):
    """
    Reqires the simulation to use the tidyHelper diffraction_monitor function above
    input_pol: 'RCP' or 'LCP'
    """
    amps = sim_data["diffraction_monitor"].amps

    # get s and p arrays with dims (orders_x, orders_y, f)
    Es = amps.sel(polarization="s").values    # complex array
    Ep = amps.sel(polarization="p").values

    ix, iy = 0, 0   # diffraction order indices
    Es_order = Es[ix, iy, :]   # shape (freqs,)
    Ep_order = Ep[ix, iy, :]

    ERCP = (Es_order + 1j * Ep_order) / np.sqrt(2)
    ELCP = (Es_order - 1j * Ep_order) / np.sqrt(2)

    I_RCP = np.abs(ERCP)**2
    I_LCP = np.abs(ELCP)**2

    if input_pol == "r" or "R":
        conv_eff = I_LCP / (I_RCP + I_LCP)
    elif input_pol == "l" or "L":
        conv_eff = I_RCP / (I_RCP + I_LCP)
    else:
        raise ValueError("input_pol must be `rcp` or `lcp`")
    
    return conv_eff