# this script will generate a dockerfile for downloading, bidsifying ABCD data
# pre requisites
# python -m pip install neurodocker
# python -m pip install docker

neurodocker generate docker \
            --no-print \
            -o /Users/miriedel/Desktop/GitHub/abcd_dicom2bids_docker/dockerfile_07072021 \
            --base=debian:stretch \
            --pkg-manager=apt \
            --install dcmtk jq git \
            --miniconda create_env=neuro \
              conda_install='python=3.5.2' \
              pip_install='cffi==1.14.3 cryptography==3.2.1 pycparser==2.20
                           six==1.15.0 numpy==1.18.5 pandas==0.24.2 awscli
                           bids-validator==1.5.7 dcm2bids==2.1.4 docopt==0.6.2
                           future==0.18.2 nibabel==3.0.2 num2words==0.5.10
                           patsy==0.5.1 pybids==0.12.4 click==7.1.2
                           python-dateutil==2.8.1 pytz==2020.4 scipy==1.4.1
                           SQLAlchemy==1.3.20' \
            --workdir=/opt/abcd-dicom2bids \
            --run-bash 'git clone https://github.com/DCAN-Labs/abcd-dicom2bids.git /opt/abcd-dicom2bids' \
            --dcm2niix version=latest method=source \
            --matlabmcr version=2018a method=binaries \
            --fsl version=5.0.10 method=binaries \
            --add-to-entrypoint "source activate /opt/miniconda-latest/envs/neuro" \
            --entrypoint "/neurodocker/startup.sh python3 /opt/abcd_dicom2bids_docker/entrypoint.py" \
            --workdir=/opt/abcd_dicom2bids_docker \
            --run-bash 'git clone https://github.com/NBCLab/abcd_dicom2bids_docker.git /opt/abcd_dicom2bids_docker' \
            --run-bash 'mkdir /work/; mkdir /data/; mkdir /out/'


docker build -t abcddicom2bids - < /Users/miriedel/Desktop/GitHub/abcd_dicom2bids_docker/dockerfile_07072021
