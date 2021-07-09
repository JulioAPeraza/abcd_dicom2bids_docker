import os
import os.path as op
import argparse


def get_parser():
    parser = argparse.ArgumentParser(description='Downloads ABCD participant'
             'data and converts to BIDS format')
    parser.add_argument('--subjects', required=True, dest='subs')
    parser.add_argument('--modalities', required=False, dest='modalities', default=['anat', 'func'])
    return parser


def main(argv=None):

    args = get_parser().parse_args(argv)

    for i in args.modalities:
        if i not in ['anat', 'func', 'dwi']:
            raise ValueError('{} not a supported modality!'.format(i))

    subject_text_file = '/work/subject_ids.txt'
    with open(subject_text_file, 'w') as fo:
        for sub in args.subs:
            fo.write('{}\n'.format(sub))

    cmd="python3 /opt/abcd-dicom2bids/abcd2bids.py /opt/fsl-5.0.10/ /opt/matlabmcr-2018a/v94/ \
      --subject-list {subject_text_file} \
      --modalities '{modalities}' \
      --qc /data/qc_spreadsheet.txt \
      --output /out/ \
      --config /data/config_file.ini \
      --remove".format(subject_text_file=subject_text_file, modalities="' '".join(args.modalities))

    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    main()
