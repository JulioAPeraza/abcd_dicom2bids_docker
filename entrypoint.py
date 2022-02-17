import argparse
import os

# Constant: List of function names of steps 1-5 in the list above
STEP_NAMES = ["create_good_and_bad_series_table", "download_nda_data",
              "unpack_and_setup", "correct_jsons", "validate_bids"]

def get_parser():
    parser = argparse.ArgumentParser(
        description="Downloads ABCD participant" "data and converts to BIDS format"
    )
    parser.add_argument("--subjects", required=True, dest="subs", nargs="+")
    parser.add_argument(
        "--modalities",
        required=False,
        dest="modalities",
        nargs="+",
        type=str,
        default=["anat", "func"],
    )
    parser.add_argument(
        "--sessions",
        required=False,
        dest="sessions",
        nargs="+",
        default=["baseline_year_1_arm_1", "2_year_follow_up_y_arm_1"],
    )
    parser.add_argument(
        "--stop_before",
        dest="stop_before",
        choices=STEP_NAMES,
        default=STEP_NAMES[4],
        help=("Give the name of the step in the wrapper to stop "
              "at. All steps before will be run. Here are the "
              "names of all of the steps, in order from first to last: "
              + ", ".join(STEP_NAMES))
    )
    return parser


def main(argv=None):

    args = get_parser().parse_args(argv)

    subject_text_file = "/work/subject_ids.txt"
    with open(subject_text_file, "w") as fo:
        for sub in args.subs:
            fo.write("{}\n".format(sub))

    modalities = "'{}'".format(" ".join(args.modalities).replace(" ", "' '"))
    sessions = "{}".format(" ".join(args.sessions))

    # --remove
    cmd = "python3 /opt/abcd-dicom2bids/abcd2bids.py /opt/fsl-5.0.10/ /opt/matlabmcr-2016b/v91/ \
      --subject-list {subject_text_file} \
      --modalities {modalities} \
      --sessions {sessions} \
      --temp /work \
      --download /raw \
      --qc /data/qc_spreadsheet.txt \
      --stop_before {stop_before} \
      --output /out/ \
      --config /data/config_file.ini \
      ".format(
        subject_text_file=subject_text_file, modalities=modalities, sessions=sessions,stop_before=args.stop_before
    )

    print(cmd)
    os.system(cmd)


if __name__ == "__main__":
    main()
