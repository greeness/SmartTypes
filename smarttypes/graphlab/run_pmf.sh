
GROUPS=100

cd '/home/ubuntu/graphlabapi/release/demoapps/pmf/'

./pmf smarttypes_pmf 10 --float=true --scheduler="round_robin(max_iterations=10,block_size=1)" \
--ncpus=7 --binaryoutput=true --zero=true --D=$GROUPS --desired_factor_sparsity=0.9 --lambda=0.06 \
> pmf_job.`/bin/date +"%Y_%m_%d_%H"`.txt &

mv smarttypes_pmf$GROUPS.out /home/timmyt/projects/smarttypes/smarttypes/graphlab/smarttypes_pmf.out

#./pmf smarttypes_pmf $METHOD --float=true --scheduler="round_robin(max_iterations=30,block_size=1)" \
#--burn_in=10 --ncpus=7 --binaryoutput=true --zero=true --D=$GROUPS \
#> pmf_job.`/bin/date +"%Y_%m_%d_%H"`.txt &
