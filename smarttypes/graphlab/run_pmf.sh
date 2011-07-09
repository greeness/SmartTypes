cd /home/ubuntu/graphlabapi/release/demoapps/pmf/

./pmf smarttypes_pmf 1 --float=true --scheduler="round_robin(max_iterations=30,block_size=1)" \
--burn_in=10 --ncpus=4 --binaryoutput=true --zero=true --D=2 --minval=0 --maxval=1

