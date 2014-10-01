#!/usr/bin/env python3

from numba import jit
from contracts import contract

from glob import glob
import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import h5py

#from scipy.ndimage.filters import convolve

HDF5_SNAPSHOTS_DATA_PATH = '/DataSamples/Snapshots/Data'
HDF5_FREQUENCIES_DATA_PATH = '/DataSamples/Frequencies/Data'

COLORS_GRID = ((
    # http://blog.mollietaylor.com/2012/10/color-blindness-and-palette-choice.html
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

def get_hdf5_grid():
    '''Returns a dict()'''
    @contract(filename_template='str', returns='list[10](list[10](str))')
    def get_filename_list(filename_template):
        return [[
            glob(filename_template.format(
                sth=row_i,
                cth=col_i,
            ))[0]
        for col_i in range(10)]
        for row_i in range(10)]

    def open_h5py_files(filename_list_list):
        return [[h5py.File(filename)
                 for filename in filename_list]
                 for filename_list in filename_list_list]

    data_dir = '../../strife-notebook/data/'
    filename_templates = [
        'avigdor-utcepoch-*-sth-{sth}-cth-{cth}-ccost-10.json*.h5',
        'avigdor-utcepoch-*-sth-{sth}-cth-{cth}-ccost-30.json*.h5',
        'avigdor-utcepoch-*-sth-{sth}-cth-{cth}-ccost-36-D-0.2.json-*.h5',
        'avigdor-utcepoch-*-sth-{sth}-cth-{cth}-ccost-36-D-0.4.json-*.h5',
    ]
    [
        filename_template_ccost_10,
        filename_template_ccost_30,
        filename_template_diffusion_02,
        filename_template_diffusion_04,
    ] = [data_dir + n for n in filename_templates]

    return dict(
        ccost_10 = open_h5py_files(get_filename_list(filename_template_ccost_10)),
        ccost_30 = open_h5py_files(get_filename_list(filename_template_ccost_30)),
        diffusion_02 = open_h5py_files(get_filename_list(filename_template_diffusion_02)),
        diffusion_04 = open_h5py_files(get_filename_list(filename_template_diffusion_04)),
    )

def beaut(fig, axes):
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

    beaut(fig, axes)

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

    beaut(fig, axes)

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
@jit('int32[:,:](int32[:,:],int32[:,:])', nopython=True)
def count_neighbors_of_strains(a_board, res):
    row_num, col_num = a_board.shape
    for central_strain in range(4,8):
        for neighbor_strain in range(4,8):
            for central_row_i in range(row_num):
                for central_col_i in range(col_num):
                    for delta_row_i in range(-1, 2):
                        for delta_col_i in range(-1, 2):
                            neighbor_row_i = central_row_i + delta_row_i
                            neighbor_col_i = central_col_i + delta_col_i
                            if neighbor_row_i >= row_num:
                                neighbor_row_i = neighbor_row_i - row_num
                            if neighbor_col_i >= col_num:
                                neighbor_col_i = neighbor_col_i - col_num
                            is_central_strain = central_strain == a_board[central_row_i, central_col_i]
                            if is_central_strain:
                                is_neighbor_strain = neighbor_strain == a_board[neighbor_row_i, neighbor_col_i]
                                if is_neighbor_strain:
                                    res[central_strain, neighbor_strain] += 1
    return res


def test_neigbor_count():
    test = h5py.File(
        # data filename
        '../../../strife-data/data/avigdor-sth-5-cth-5-ccost-10.json-1361510454900658000-2000-603157824.h5'
    )[
        # hdf5 data set path name
        '/DataSamples/Snapshots/Data'
    ] # sample #150

    #print(test[5:10,5:10])
    for i in range(1):
        print(i)
        a = test[i][...]
        res = np.zeros((8,8), dtype='int32')
        count_neighbors_of_strains(a, res)
        print(res)
        print(i)


def main():
    print(count_neighbors_of_strains.inspect_types())
    #ff_dict = get_hdf5_grid()

    #print('make freqs plots')

    #data_set_name_list = ['ccost_10', 'ccost_30', 'diffusion_02', 'diffusion_04']

    #for data_set_name in data_set_name_list:
    #    make_freqs_plots(ff_dict[data_set]);
    #    make_pngs(ff_dict[data_set_name], data_set_name)
    #    make_video(data_set_name)

    test_neigbor_count()


if __name__ == '__main__':
    main()
