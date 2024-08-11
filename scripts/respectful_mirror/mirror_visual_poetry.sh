source ../set_env_vars.sh
pushd $project_dir
source activate $conda_env



switch_on=true
if $switch_on; then

bash init_project.sh

fi



switch_on=true
if $switch_on; then

python $project_dir/src/respectful_mirror/build_directory_tree.py \
    --config-path $project_dir/configs/respectful_mirror \
    --config-name visual_poetry.yaml

fi


switch_on=true
if $switch_on; then

python $project_dir/src/respectful_mirror/mirror_data.py \
    --config-path $project_dir/configs/respectful_mirror \
    --config-name visual_poetry.yaml

fi
