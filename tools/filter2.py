#!/usr/bin/env python

from pandas import read_csv
import argparse, sys

def filterIQM(argv=sys.argv):

    # Read data here
    ## T1w
    df = read_csv('/home/soffiafdz/mriqception/test_data/T1w.csv')
    cols = df.columns
    cols = cols.map(lambda x: x.replace(".", "_"))
    df.columns = cols

    parser = argparse.ArgumentParser(description = "Process the IQM's to sort.")

    parser.add_argument('-s', '--snr',
        help='Filter IQM: Signal-to-Noise ratio',
        type=str, metavar="[ == | <= | >=] SNR",
        dest='snr', action='append')

    parser.add_argument('-sg', '--snr_gm',
        help='Filter IQM: Signal-to-Noise ratio (GM)',
        type=str, metavar="[ == | <= | >=] SNR_GM",
        dest='snrg', action='append')

    parser.add_argument('-sw', '--snr_wm',
        help='Filter IQM: Signal-to-Noise ratio (WM)',
        type=str, metavar="[ == | <= | >=] SNR (WM)",
        dest='snrw', action='append')

    parser.add_argument('-sc', '--snr_csf',
        help='Filter IQM: Signal-to-Noise ratio (CSF)',
        type=str, metavar="[ == | <= | >=] SNR_CSF",
        dest='snrc', action='append')

    parser.add_argument('-c', '--cnr',
        help='Filter IQM: Contrast-to-Noise ratio',
        type=str, metavar="[ == | <= | >=] CNR",
        dest='cnr', action='append')

    parser.add_argument('-ef', '--efc',
        help='Filter IQM: Entropy of voxels',
        type=str, metavar="[ == | <= | >=] EFC",
        dest='efc', action='append')

    parser.add_argument('-fw', '--fwhm',
        help='Filter IQM: Full-width half maximum smoothness',
        type=str, metavar="[ == | <= | >=] FWHM",
        dest='fwhm', action='append')

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
            args.snr = ['snr_total' + s for s in args.snr]
            query += args.snr
        if args.snrg is not None:
            args.snrg = ['snr_gm' + s for s in args.snrw]
            query += args.snrg
        if args.snrw is not None:
            args.snrw = ['snr_wm' + s for s in args.snrg]
            query += args.snrw
        if args.snrc is not None:
            args.snrc = ['snr_csf' + s for s in args.snrc]
            query += args.snrc
        if args.cnr is not None:
            args.cnr = ['cnr' + s for s in args.cnr]
            query += args.cnr
        if args.efc is not None:
            args.efc = ['efc' + s for s in args.efc]
            query += args.efc
        if args.fwhm is not None:
            args.fwhm = ['fwhm_avg' + s for s in args.fwhm]
            query += args.fwhm
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
