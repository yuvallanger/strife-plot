#!/usr/bin/env python3

from __future__ import print_function

import os
import sys
from glob import glob

# import contracts
# from contracts import contract

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import h5py
from numba import jit

# from scipy.ndimage.filters import convolve

# contracts.disable_all()

DATA_DIR_PATH = 'data/'

HDF5_SNAPSHOTS_DATA_PATH = '/DataSamples/Snapshots/Data'
HDF5_FREQUENCIES_DATA_PATH = '/DataSamples/Frequencies/Data'

# http://blog.mollietaylor.com/2012/10/color-blindness-and-palette-choice.html
COLORS_GRID = (
    (
        ('#0875C2'),
        ('#6BA8D4'),
        ('#3288C4'),
        ('#054F83'),
        ('#023458'),
    ),
    (
        ('#FF0700'),
        ('#FF7D79'),
        ('#FF3A35'),
        ('#CC0500'),
        ('#890300'),
    ),
    (
        ('#00DB0E'),
        ('#6DE575'),
        ('#2DDC39'),
        ('#00A00A'),
        ('#006C07'),
    ),
    (
        ('#FF9000'),
        ('#FFC579'),
        ('#FFA735'),
        ('#CC7300'),
        ('#894D00'),
    ),
)


STRAINS_MAPPING = {
    # Checked int <-> strain.
    4: dict(strain='S1R1', color=COLORS_GRID[0][0]),
    5: dict(strain='S1R2', color=COLORS_GRID[1][0]),
    6: dict(strain='S2R1', color=COLORS_GRID[2][0]),
    7: dict(strain='S2R2', color=COLORS_GRID[3][0]),
}


#@contract(data_dir_path='str', returns='dict(str:(list[10](list[10])))')
def get_hdf5_grid():
    """Return a dict(str:list[10](list[10])."""

    return {
        sim_series: [
            [
                h5py.File(glob(
                    DATA_DIR_PATH + filename_template.format(
                        sth=row_i,
                        cth=col_i,
                    ))[0]
                )
                for col_i in range(10)
            ]
            for row_i in range(10)
        ]
        for sim_series, filename_template in zip(
            (
                'ccost_10',
                'ccost_30',
                'diffusion_02',
                'diffusion_04',
            ),
            (
                'avigdor-utcepoch-*-sth-{sth}-cth-{cth}-ccost-10.json*.h5',
                'avigdor-utcepoch-*-sth-{sth}-cth-{cth}-ccost-30.json*.h5',
                'avigdor-utcepoch-*-sth-{sth}-cth-{cth}-ccost-36-D-0.2.json-*.h5',
                'avigdor-utcepoch-*-sth-{sth}-cth-{cth}-ccost-36-D-0.4.json-*.h5',
            )
        )
    }


#@contract(fig=mpl.figure.Figure, axes='list[10](list[10])')
def beautify(fig, axes):
    for row_i, axes_row in enumerate(axes):
        for col_i, ax in enumerate(axes_row):
            ax.set_xticks([])
            ax.set_yticks([])

            if col_i == 0:
                ax.set_ylabel(str(row_i))

            if row_i == 9:
                ax.set_xlabel(str(col_i))

    plt.figtext(
        0.5,
        0,
        "public goods effect threshold",
        figure=fig,
        fontsize=17,
        horizontalalignment='center',
        verticalalignment='top',
    )


    plt.figtext(
        0,
        0.5,
        "quorum sensing threshold",
        figure=fig,
        fontsize=17,
        horizontalalignment='right',
        verticalalignment='center',
        rotation=90,
    )

    fig.tight_layout()


def make_plots(data, plotter):
    fig, axes = plt.subplots(
        figsize=(13,13),
        nrows=10,
        ncols=10,
    )

    for row_i in range(10):
        for col_i in range(10):
                plotter(axes, data, row_i, col_i)

    beautify(fig, axes)

    return fig, axes


def get_simulation_freqs_data_grid(ff_grid):
    return [[
        # 0:4 never existed in the simulation.
        # All mutations are on the S and R loci, never on C locus.
        # 0:4 are all C deactivated allele. 4:8 are all C activated allele.
        ff[HDF5_FREQUENCIES_DATA_PATH]
    for ff in ff_list]
    for ff_list in ff_grid]


def freqs_plotter(axes, freqs_data, sth, cth):
    for strain_i, strain_attr in STRAINS_MAPPING.items():
        axes[sth][cth].plot(
            freqs_data[sth][cth][:, strain_i],
            strain_attr.get('pattern', '-'),
            label=strain_attr.get('strain', strain_i),
            color=strain_attr['color']
        )


def make_freqs_plots(ff_list_list):
    data = get_simulation_freqs_data_grid(ff_list_list)
    fig, axes = make_plots(data, freqs_plotter)

    return fig, axes


def animate_func(ff_list_list, im_list_list, snapshot_i):
    for im_list, ff_list in zip(im_list_list, ff_list_list):
        for im, ff in zip(im_list, ff_list):
            im.set_data(ff[HDF5_SNAPSHOTS_DATA_PATH][snapshot_i])


def make_pngs(ff_list_list, fname):
    # make a color map of fixed colors
    # https://stackoverflow.com/questions/9707676/defining-a-discrete-colormap-for-imshow-in-matplotlib
    cmap = mpl.colors.ListedColormap([STRAINS_MAPPING[i]['color'] for i in range(4,8)])
    bounds = [4, 5, 6, 7, 8]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    fig, axes = plt.subplots(
        figsize=(13,13),
        nrows=10,
        ncols=10,
    )

    im_list_list = [[
        # tell imshow about color map so that only set colors are used
        ax.imshow(
            ff[HDF5_SNAPSHOTS_DATA_PATH][0],
            interpolation='nearest',
            origin='lower',
            cmap=cmap,
            norm=norm,
        )
        for ff, ax in zip(ff_row, axes_row)]
        for ff_row, axes_row in zip(ff_list_list, axes)]

    beautify(fig, axes)

    for snapshot_i in range(ff_list_list[0][0][HDF5_SNAPSHOTS_DATA_PATH].shape[0]):
        animate_func(ff_list_list, im_list_list, snapshot_i)
        temp_fname = '_tmp{:03d}'.format(snapshot_i)+fname+'.png'
        fig.savefig(temp_fname)


def make_video(fname):
    print('Making movie animation.mpg - this make take a while')
    os.system(
        "mencoder mf://_tmp*-" +fname + ".png "
        "-mf type=png "
        "-oac copy "
        "-ovc lavc "
        "-lavcopts vcodec=ffv1 "
        "-o video-" + fname + ".mp4"
    )


#@contract(a_board='array[NxN](int32),N>0', returns='dict[4](int: array[NxN](int32),N>0)')

@jit('void(int32[:,:,:], int32[:,:,:])', nopython=True)
def jitted_count_neighbors(a_board, res_board):
    snapshot_num, row_num, col_num = a_board.shape
    for snapshot_i in range(snapshot_num):
        for central_strain in range(4,8):
            for neighbor_strain in range(4,8):
                for central_row_i in range(row_num):
                    for central_col_i in range(col_num):
                        for delta_row_i in range(-1, 2):
                            for delta_col_i in range(-1, 2):
                                neighbor_row_i = (central_row_i + delta_row_i) % row_num
                                neighbor_col_i = (central_col_i + delta_col_i) % col_num

                                is_central_strain = central_strain == a_board[snapshot_i, central_row_i, central_col_i]
                                is_neighbor_strain = neighbor_strain == a_board[snapshot_i, neighbor_row_i, neighbor_col_i]

                                if is_central_strain and is_neighbor_strain:
                                    res_board[snapshot_i, central_strain, neighbor_strain] = res_board[snapshot_i, central_strain, neighbor_strain] + 1


@jit('int32[:,:,:](int32[:,:,:])')
def count_neighbors(a_board):
    """Return count of neighbors of each strain for each strain of central cell

    For each board snapshot `snapshot_i` and for each cell of strain
    `central_strain`, count the total number of cells of each cell of strain
    `neighbor_strain` which are inside the Moore neighborhood around cells of
    strain `central_strain`.
    """
    res_shape = a_board.shape[0], 8, 8
    res_board = np.zeros(res_shape, dtype='int32')
    jitted_count_neighbors(a_board, res_board)
    return res_board


def count_total_strains(a_board):
    res = np.sum(a_board == strain_enum, axis=(1,2))
    for strain_enum in range(4, 8):
        res = np.vstack(res, sum(a_board == strain_enum), axis=(1,2))
    return res



def count_relative_neighbors(a_board):
    neighbors_count = count_neighbors(a_board)
    total_count_total_strains(a_board)


def test_neighbors_count():
    test = h5py.File(
        # data filename
        'data/avigdor-sth-5-cth-5-ccost-10.json-1361510454900658000-2000-603157824.h5'
    )[
        # hdf5 data set path name
        '/DataSamples/Snapshots/Data'
    ][...]

    #total_strain_count_board = count_strains()

    neighbors_count = count_neighbors(test)
    print(neighbors_count)


def test():
    test_neighbors_count()


def main():
    test()
    #ff_dict = get_hdf5_grid()

    #print('make freqs plots')

    #data_set_name_list = ['ccost_10', 'ccost_30', 'diffusion_02', 'diffusion_04']

    #for data_set_name in data_set_name_list:
    #    make_freqs_plots(ff_dict[data_set]);
    #    make_pngs(ff_dict[data_set_name], data_set_name)
    #    make_video(data_set_name)



if __name__ == '__main__':
    main()
