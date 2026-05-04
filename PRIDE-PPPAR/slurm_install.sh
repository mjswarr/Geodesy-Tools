#!/bin/bash

#SBATCH --job-name=MJS_PPP_INSTL          # Job name
#SBATCH --output=test_%j.log     # Standard output and error log
#SBATCH --nodes=1                # Request one node
#SBATCH --ntasks-per-node=1      # Request 1 task per node
#SBATCH --cpus-per-task=12
#SBATCH --time=48:00:00          # Time limit hrs:min:sec (e.g., 1 hour)
#SBATCH --mem=24GB               # RAM per node
#SBATCH --partition=cpu(all)     # Specify the CPU partition

# Load Conda module
module load conda

# Create Conda environment
conda create -n my_env3 -c conda-forge compilers python=3.7 -y
#conda env create -n my_env3 -f gfortran.yml python=3.7 -y
#conda create -n my_env3 python=3.7 -y

# Activate Conda environment
source activate my_env3

# Install necessary packages in Conda environment
conda install -n my_env3 numpy requests
#conda install conda-forge::gfortran_linux-64

# Create .netrc File to Authorize NASA CDDIS Access
#echo machine urs.earthdata.nasa.gov login mswarr password mooGrizz123 >> ~/.netrc

# Change Authorization of .netrc File
#chmod 0600 ~/.netrc

# Install EarthScope Command Line Tools
#pip install earthscope-cli

# Log Into EarthScope Data Server
## This will require you to copy and paste the displayed link in your web browser to confirm access ##
#es sso login

# Your job commands go below this line
#python get_rinex.py
./install.sh

# Deactivate Conda environment
conda deactivate

# Unload Conda module
module purge
