source ../set_env_vars.sh
pushd $project_dir
source activate $conda_env


mkdir data
mkdir data/respectful_mirror
mkdir src
mkdir src/respectful_mirror
mkdir config
mkdir configs/respectful_mirror


# these are simple dependencies so no need to overengineer version replication
pip install omegaconf
pip install hydra-core
pip install beautifulsoup4