#PBS -N GridSearcher
#PBS -d /Users/chris/gridsearcher2/models
#PBS -l mem=4g
#PBS -l file=10g
## Queues: vshort (10min), short (1h 30min), medium (24h), long (1 week)
#PBS -q medium
#PBS -j oe

source /etc/profile

echo "Running job $PBS_ARRAYID"
python /Users/chris/gridsearcher2/scripts/runner.py $PBS_ARRAYID
echo "Done"
