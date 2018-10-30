#!/usr/bin/env python3
"""Example of plotting slices of a field with yt and matplotlib manipulation of the plot"""


# ========================================================================
#
# Imports
#
# ========================================================================
import numpy as np
import yt
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import SymmetricalLogLocator
from matplotlib.backends.backend_pdf import PdfPages


# ========================================================================
#
# Function definitions
#
# ========================================================================
def plot_ds(fdir, field="x_velocity"):

    # Load the data
    ds = yt.load(fdir, unit_system="mks")

    # Setup
    L = (ds.domain_right_edge - ds.domain_left_edge).d
    width = L[0]
    res = 512
    zlocs = np.array([0.0525, 0.0775, 0.1025, 0.1275, 0.1525])
    fname = "slices.pdf"

    with PdfPages(fname) as pdf:
        plt.close("all")
        plt.rc("text", usetex=True)
        linthresh = 1e-3

        # Get a slice in x
        slc = yt.SlicePlot(ds, "x", fields=[field])
        frb = slc.data_source.to_frb(width, res)
        x_slc = np.array(frb[field])

        fig0 = plt.figure(0)
        ax0 = fig0.add_subplot(111)
        im = ax0.imshow(
            x_slc,
            origin="lower",
            extent=[
                ds.domain_left_edge.d[0],
                ds.domain_right_edge.d[0],
                ds.domain_left_edge.d[2],
                ds.domain_right_edge.d[2],
            ],
            aspect="equal",
            cmap="Spectral_r",
            norm=colors.SymLogNorm(
                linthresh=linthresh, linscale=0.5, vmin=x_slc.min(), vmax=x_slc.max()
            ),
        )
        cbar = plt.colorbar(
            im, ax=ax0, ticks=SymmetricalLogLocator(linthresh=linthresh, base=10)
        )
        cbar.ax.set_title(r"$u$")

        for zloc in zlocs:
            ax0.plot(
                [ds.domain_left_edge.d[0], ds.domain_right_edge.d[0]],
                [zloc, zloc],
                color="w",
                lw=1,
                ls="--",
            )

        ax0.set_xlabel(r"$y~[\mathrm{m}]$", fontsize=22, fontweight="bold")
        ax0.set_ylabel(r"$z~[\mathrm{m}]$", fontsize=22, fontweight="bold")
        plt.setp(ax0.get_xmajorticklabels(), fontsize=18)
        plt.setp(ax0.get_ymajorticklabels(), fontsize=18)
        fig0.subplots_adjust(bottom=0.15)
        fig0.subplots_adjust(left=0.17)
        pdf.savefig(dpi=300)

        # Get slices in z
        for k, zloc in enumerate(zlocs):
            slc = yt.SlicePlot(ds, "z", fields=[field], center=[0, 0, zloc])
            frb = slc.data_source.to_frb(width, res)
            z_slc = np.array(frb[field])

            fig0 = plt.figure(k + 1)
            ax0 = fig0.add_subplot(111)
            im = ax0.imshow(
                z_slc,
                origin="lower",
                extent=[
                    ds.domain_left_edge.d[0],
                    ds.domain_right_edge.d[0],
                    ds.domain_left_edge.d[1],
                    ds.domain_right_edge.d[1],
                ],
                aspect="equal",
                cmap="Spectral_r",
                norm=colors.SymLogNorm(
                    linthresh=linthresh,
                    linscale=0.5,
                    vmin=x_slc.min(),
                    vmax=x_slc.max(),
                ),
            )
            cbar = plt.colorbar(
                im, ax=ax0, ticks=SymmetricalLogLocator(linthresh=linthresh, base=10)
            )
            cbar.ax.set_title(r"$u$")

            ax0.set_xlabel(r"$x~[\mathrm{m}]$", fontsize=22, fontweight="bold")
            ax0.set_ylabel(r"$y~[\mathrm{m}]$", fontsize=22, fontweight="bold")
            plt.setp(ax0.get_xmajorticklabels(), fontsize=18)
            plt.setp(ax0.get_ymajorticklabels(), fontsize=18)
            fig0.subplots_adjust(bottom=0.15)
            fig0.subplots_adjust(left=0.17)
            pdf.savefig(dpi=300)
