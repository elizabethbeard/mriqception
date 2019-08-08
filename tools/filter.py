#!/usr/bin/env python

from pandas import read_csv
import argparse, sys


def filterIQM(argv=sys.argv):

    # Read data here
    ## BOLD
    df = read_csv('/home/soffiafdz/mriqception/test_data/bold_all.csv')
    cols = df.columns
    cols = cols.map(lambda x: x.replace(".", "_"))
    df.columns = cols

    parser = argparse.ArgumentParser(description = "Process the IQM's to sort.")

    parser.add_argument('-s', '--snr',
        help='Filter IQM: Signal-to-Noise ratio',
        type=str, metavar="[ == | <= | >=] SNR",
        dest='snr', action='append')

    parser.add_argument('-t', '--tsnr',
        help='Filter IQM: Temporal Signal-to-Noise ratio',
        type=str, metavar="[ == | <= | >=] TSNR",
        dest='tsnr', action='append')

    parser.add_argument('-d', '--dvars',
        help='Filter IQM: Temporal Derivatives Variance (DVAR)',
        type=str, metavar="[ == | <= | >=] DVAR",
        dest='dvars', action='append')

    parser.add_argument('-fw', '--fwhm',
        help='Filter IQM: Full-width half maximum smoothness',
        type=str, metavar="[ == | <= | >=] FWHM",
        dest='fwhm', action='append')

    parser.add_argument('-m', '--fd',
        help='Filter IQM: Framewise displacement',
        type=str, metavar="[ == | <= | >=] FD",
        dest='fd', action='append')

    parser.add_argument('-gx', '--gsr_x',
        help='Filter IQM: Ghost-to-Signal ratio (X axis)',
        type=str, metavar="[ == | <= | >=] gsr_x",
        dest='gsrx', action='append')

    parser.add_argument('-gy', '--gsr_y',
        help='Filter IQM: Ghost-to-Signal ratio (Y axis)',
        type=str, metavar="[ == | <= | >=] gsr_y",
        dest='gsry', action='append')

    parser.add_argument('-e', '--te',
        help='Filter Acquisition Parameter: Echo time',
        type=str, metavar="[ == | <= | >=] TE",
        dest='te', action='append')

    parser.add_argument('-r', '--tr',
        help='Filter Acquisition Parameter: Repetition time',
        type=str, metavar="[ == | <= | >=] TR",
        dest='tr', action='append')

    parser.add_argument('-T', '--Tesla',
        help='Filter Acquisition Parameter: Magnetic Field Strength',
        type=str, metavar="[ == | <= | >=] Tesla",
        dest='tesla', action='append')

    args = parser.parse_args()

    if len(sys.argv[1:]) == 0:
        return df
    else:
        query = []
        if args.snr is not None:
            args.snr = ['snr' + s for s in args.snr]
            query += args.snr
        if args.tsnr is not None:
            args.tsnr = ['tsnr' + s for s in args.tsnr]
            query += args.tsnr
        if args.dvars is not None:
            args.dvars = ['dvars_nstd' + s for s in args.dvars]
            query += args.dvars
        if args.fwhm is not None:
            args.fwhm = ['fwhm_avg' + s for s in args.fwhm]
            query += args.fwhm
        if args.fd is not None:
            args.fd = ['fd_mean' + s for s in args.fd]
            query += args.fd
        if args.gsrx is not None:
            args.gsrx = ['gsr_x' + s for s in args.gsrx]
            query += args.gsrx
        if args.gsry is not None:
            args.gsry = ['gsr_y' + s for s in args.gsry]
            query += args.gsry
        if args.te is not None:
            args.te = ['bids_meta_EchoTime' + s for s in args.te]
            query += args.te
        if args.tr is not None:
            args.tr = ['bids_meta_RepetitionTime' + s for s in args.tr]
            query += args.tr
        if args.tesla is not None:
            args.tesla = ['bids_meta_MagneticFieldStrength' + s for s in args.tesla]
            query += args.tesla

        print(query)

        return df.query(" & ".join(query))

if __name__ == '__main__':
    sys.exit(filterIQM())
