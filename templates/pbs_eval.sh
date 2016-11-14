#PBS -N GridSearcher-Eval
#PBS -l nodes=1:ppn=4
#PBS -l mem=4g
#PBS -l file=10g
## Queues: vshort (10min), short (1h 30min), medium (24h), long (1 week)
#PBS -q short
#PBS -j oe

source /etc/profile

echo "Running job $PBS_ARRAYID"

cd $PBS_O_WORKDIR
setupATLAS
lsetup root
source $HOME/env/tid/bin/activate
python gridsearcher2/scripts/xgb_eval.py $PBS_ARRAYID

echo "Done"
