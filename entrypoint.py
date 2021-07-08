import os
import os.path as op

def get_parser():
    parser = argparse.ArgumentParser(description='Downloads ABCD participant'
             'data and converts to BIDS format')
    parser.add_argument('--subjects', required=True, dest='subs')
    parser.add_argument('--work_dir', required=False, dest='work_dir', default='~/temp')
    parser.add_argument('--modalities', required=False, dest='modalities' default=['anat', 'func'])
    parser.add_argument('--qc', required=True, dest='qc_spreadsheet')
    parser.add_argument('--config', required=True, dest='config_file')
    parser.add_argument('--out_dir', required=False, dest='out_dir', default='~/abcd/dset')
    return parser


def main(argv=None):

    args = get_parser().parse_args(argv)

    for i in args.modalities:
        if i not in ['anat', 'func', 'dwi']:
            raise ValueError('{} not a supported modality!'.format(i))

    if not op.isfile(args.qc_spreadsheet):
        raise ValueError('{} is not an existing file!'.format(args.qc_spreadsheet))

    if not op.isfile(args.config_file):
        raise ValueError('{} is not an existing file!'.format(args.config_file))

    subject_text_file = op.join(args.work_dir, 'subject_ids.txt')
    with open(subject_text_file, 'w') as fo:
        for sub in args.subs:
            fo.write('{}\n'.format(sub))

    cmd='python3 /opt/abcd-dicom2bids/abcd2bids.py /opt/fsl-5.0.10/ /opt/matlabmcr-2018a/v94/ \
      --subject-list {subject_text_file} \
      --modalities {modalities} \
      --qc {qc_spreadsheet} \
      --output {output_directory} \
      --config {config_file} \
      --remove'.format(subject_text_file=subject_text_file, modalities=args.modalities,
                       qc_spreadsheet=args.qc_spreadsheet, output_directory=args.out_dir,
                       config_file=args.config_file)

    print(cmd)

    os.system(cmd)


if __name__ == '__main__':
    main()
