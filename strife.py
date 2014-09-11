import numpy as np
import matplotlib.pyplot as plt
import h5py

from glob import glob
import os

import numpy as np
import scipy as sp
from scipy.ndimage.filters import convolve
import pandas as pd

STRAINS = (S1R1, S1R2, S2R1, s2R2,) = (4, 5, 6, 7,)

#######

colors_grid = (
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


# Checked int <-> strain.
strains = {
        4:dict(strain='S1R1', color=colors_grid[0][0]),
        5:dict(strain='S1R2', color=colors_grid[1][0]),
        6:dict(strain='S2R1', color=colors_grid[2][0]),
        7:dict(strain='S2R2', color=colors_grid[3][0]),
}

# http://blog.mollietaylor.com/2012/10/color-blindness-and-palette-choice.html

########

def get_hdf5_grid():
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

    DATA_DIR = '../../strife-notebook/data/'

    [filename_template_ccost_10,
    filename_template_ccost_30,
    filename_template_diffusion_02,
    filename_template_diffusion_04] = [DATA_DIR + n for n in
        ['avigdor-utcepoch-*-sth-{sth}-cth-{cth}-ccost-10.json*.h5',
         'avigdor-utcepoch-*-sth-{sth}-cth-{cth}-ccost-30.json*.h5',
         'avigdor-utcepoch-*-sth-{sth}-cth-{cth}-ccost-36-D-0.2.json-*.h5',
         'avigdor-utcepoch-*-sth-{sth}-cth-{cth}-ccost-36-D-0.4.json-*.h5',
         ]]

    return dict(
        ccost_10 = open_h5py_files(get_filename_list(filename_template_ccost_10)),
        ccost_30 = open_h5py_files(get_filename_list(filename_template_ccost_30)),
        diffusion_02 = open_h5py_files(get_filename_list(filename_template_diffusion_02)),
        diffusion_04 = open_h5py_files(get_filename_list(filename_template_diffusion_04)),
    )

ff_dict = get_hdf5_grid()

HDF5_SNAPSHOTS_DATA_PATH = '/DataSamples/Snapshots/Data'
HDF5_FREQUENCIES_DATA_PATH = '/DataSamples/Frequencies/Data'

########

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

########

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

########

def get_simulation_freqs_data_grid(ff_grid):
    return [[
        # 0:4 never existed in the simulation.
        # All mutations are on the S and R loci, never on C locus.
        # 0:4 are all C deactivated allele. 4:8 are all C activated allele.
        ff[HDF5_FREQUENCIES_DATA_PATH]
    for ff in ff_list]
    for ff_list in ff_grid]

########

def freqs_plotter(axes, freqs_data, sth, cth):
    for strain_i, strain_attr in strains.items():
        axes[sth][cth].plot(
            freqs_data[sth][cth][:, strain_i],
            strain_attr.get('pattern', '-'),
            label=strain_attr.get('strain', strain_i),
            color=strain_attr['color']
        )

########

def make_freqs_plots(ff_list_list):
    data = get_simulation_freqs_data_grid(ff_list_list)
    fig, axes = make_plots(data, freqs_plotter)

    return fig, axes

########

make_freqs_plots(ff_dict['ccost_10']);
make_freqs_plots(ff_dict['ccost_30']);
make_freqs_plots(ff_dict['diffusion_02']);
make_freqs_plots(ff_dict['diffusion_04']);

########

# https://stackoverflow.com/questions/9707676/defining-a-discrete-colormap-for-imshow-in-matplotlib

def animate_func(ff_list_list, im_list_list, snapshot_i):
    for im_list, ff_list in zip(im_list_list, ff_list_list):
        for im, ff in zip(im_list, ff_list):
            im.set_data(ff[HDF5_SNAPSHOTS_DATA_PATH][snapshot_i])

def make_pngs(ff_list_list, fname):
    # make a color map of fixed colors
    cmap = mpl.colors.ListedColormap([strains[i]['color'] for i in range(4,8)])
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
    print 'Making movie animation.mpg - this make take a while'
    os.system(
        "mencoder mf://_tmp*-" +fname + ".png "
        "-mf type=png "
        "-oac copy "
        "-ovc lavc "
        "-lavcopts vcodec=ffv1 "
        "-o video-" + fname + ".mp4"
    )

########

make_pngs(ff_dict['ccost_10'], 'ccost-10')
make_pngs(ff['ccost_30'], 'ccost-30')
make_pngs(ff['diffusion_02'], 'diffusion-02')
make_pngs(ff['diffusion_04'], 'diffusion-04')

########

#make_video('ccost-10')
#make_video('ccost-30')
#make_video('diffusion-02')
#make_video('diffusion-04')

########
def make_middle_counters_board(x):
    y = (((x > 99) * x) - 100)
    return (y > 0) * y

def convolved(a_board, k, strain_middle, strain_neighbor):
    def find_middle_strain():
        a = a_board == strain_middle
        return a

    def find_neighbor_strain():
        a = a_board == strain_neighbor
        return a

    a = find_middle_strain() * 10
    b = find_neighbor_strain()

    c = convolve(a + b, k, mode='wrap',)

    print strain_middle
    print strain_neighbor
    print k
    print a_board
    print a
    print b
    print c

    return c

def globity(a_board):
    k = np.array(
        [[1, 1 , 1],
         [1, 10, 1],
         [1, 1 , 1],],
        dtype='int64'
    )

    strain_board = {
        strain_middle: {
            strain_neighbor : (
                np.sum(
                    make_middle_counters_board(
                        convolved(
                            a_board=a_board,
                            k=k,
                            strain_middle=strain_middle,
                            strain_neighbor=strain_neighbor,
                        )
                    )
                )
            )
            for strain_neighbor in STRAINS
        }
        for strain_middle in STRAINS
    }

    return strain_board

def main():
    return globity(h5py.File('../../../strife-notebook/data/avigdor-sth-5-cth-5-ccost-10.json-1361510454900658000-2000-603157824.h5')['/DataSamples/Snapshots/Data'][150])

if __name__ == '__main__':
    main()
