import os
import os.path as op
import argparse


def get_parser():
    parser = argparse.ArgumentParser(description='Downloads ABCD participant'
             'data and converts to BIDS format')
    parser.add_argument('--subjects', required=True, dest='subs', nargs='+')
    parser.add_argument('--modalities', required=False, dest='modalities', nargs='+', type=str, default="'anat', 'func'")
    parser.add_argument('--sessions', required=False, dest='sessions', nargs='+', default=['baseline_year_1_arm_1', '2_year_follow_up_y_arm_1'])
    return parser


def main(argv=None):

    args = get_parser().parse_args(argv)

    subject_text_file = '/work/subject_ids.txt'
    with open(subject_text_file, 'w') as fo:
        for sub in args.subs:
            fo.write('{}\n'.format(sub))

    print(args.modalities)
    print(type(args.modalities))
    cmd="python3 /opt/abcd-dicom2bids/abcd2bids.py /opt/fsl-5.0.10/ /opt/matlabmcr-2018a/v94/ \
      --subject-list {subject_text_file} \
      --modalities {modalities} \
      --sessions {sessions} \
      --temp /work \
      --qc /data/qc_spreadsheet.txt \
      --output /out/ \
      --config /data/config_file.ini \
      --remove".format(subject_text_file=subject_text_file,
                       modalities=args.modalities,
                       sessions=args.sessions)

    os.system(cmd)


if __name__ == '__main__':
    main()
