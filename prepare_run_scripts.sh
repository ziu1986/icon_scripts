#!/bin/bash
scripts_src=~/scripts
build_dir=~/build
cp ${scripts_src}/exp.jsbalone_R2B4_sfa ${build_dir}/run && cd ${build_dir} && ./make_runscripts -s jsbalone_R2B4_sfa && cd ${build_dir}/run
