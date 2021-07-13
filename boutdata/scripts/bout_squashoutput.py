#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

"""
Collect all data from BOUT.dmp.* files and create a single output file.

Output file named BOUT.dmp.nc by default

Useful because this discards ghost cell data (that is only useful for debugging)
and because single files are quicker to download.

"""

try:
    import argcomplete
except ImportError:
    argcomplete = None
import boutdata.squashoutput as squash


def main():
    """
    Call the squashoutput function using arguments from command line - used to provide a
    command-line executable using setuptools entry_points in setup.py
    """

    import argparse

    try:
        import argcomplete
    except ImportError:
        argcomplete = None

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description=(
            __doc__
            + "\n\n"
            + squash.__doc__
            + "\n\nNote: the --tind, --xind, --yind and --zind command line arguments "
            "are converted\ndirectly to Python slice() objects and so use exclusive "
            "'stop' values. They can be\npassed up to 3 values: [stop], [start, stop], "
            "or [start, stop, step]."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    def str_to_bool(string):
        return string.lower() == "true" or string.lower() == "t"

    def int_or_none(string):
        try:
            return int(string)
        except ValueError:
            if string.lower() == "none" or string.lower() == "n":
                return None
            else:
                raise

    parser.add_argument("datadir", nargs="?", default=".")
    parser.add_argument("--outputname", default="BOUT.dmp.nc")
    parser.add_argument("--tind", type=int_or_none, nargs="*", default=[None])
    parser.add_argument("--xind", type=int_or_none, nargs="*", default=[None])
    parser.add_argument("--yind", type=int_or_none, nargs="*", default=[None])
    parser.add_argument("--zind", type=int_or_none, nargs="*", default=[None])
    parser.add_argument("-s", "--singleprecision", action="store_true", default=False)
    parser.add_argument("-c", "--compress", action="store_true", default=False)
    parser.add_argument("-l", "--complevel", type=int_or_none, default=None)
    parser.add_argument(
        "-i", "--least-significant-digit", type=int_or_none, default=None
    )
    parser.add_argument("-q", "--quiet", action="store_true", default=False)
    parser.add_argument("-a", "--append", action="store_true", default=False)
    parser.add_argument("-d", "--delete", action="store_true", default=False)
    parser.add_argument("--tind_auto", action="store_true", default=False)
    parser.add_argument(
        "-p",
        "--parallel",
        type=int,
        default=False,
        help="Read data in parallel. Value is the number of processes to use, pass 0 "
        "to use as many as there are physical cores.",
    )
    parser.add_argument(
        "-t",
        "--time_split_size",
        type=int,
        default=None,
        help="By default no splitting is done. If an integer value is passed, the "
        "output is split into files with length in the t-dimension equal to that "
        "value. The outputs are labelled by prefacing a counter (starting by default "
        "at 0, but see time_split_first_label) to the file name before the .nc suffix.",
    )
    parser.add_argument(
        "--time_split_first_label",
        type=int,
        default=0,
        help="Value at which to start the counter labelling output files when "
        "time_split_size is used.",
    )

    if argcomplete:
        argcomplete.autocomplete(parser)

    args = parser.parse_args()

    for ind in "txyz":
        args.__dict__[ind + "ind"] = slice(*args.__dict__[ind + "ind"])
    # Call the function, using command line arguments
    squash.squashoutput(**args.__dict__)


if __name__ == "__main__":
    main()
