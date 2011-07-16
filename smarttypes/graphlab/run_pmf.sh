
GROUPS=200
METHOD=1

cd /home/ubuntu/graphlabapi/release/demoapps/pmf/

./pmf smarttypes_pmf $METHOD --float=true --scheduler="round_robin(max_iterations=30,block_size=1)" \
--burn_in=10 --ncpus=7 --binaryoutput=true --zero=true --D=$GROUPS \
> pmf_method$METHOD_job.txt &

#--minval=0 --maxval=1
#mv smarttypes_pmf$GROUPS.out /home/timmyt/projects/smarttypes/smarttypes/graphlab/smarttypes_pmf.out