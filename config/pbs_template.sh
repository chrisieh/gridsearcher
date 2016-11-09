#PBS -N {name}
#PBS -d {workdir}
#PBS -l nodes=1:ppn=4
#PBS -l mem={req_mem}
#PBS -l file={req_file}
## Queues: vshort (10min), short (1h 30min), medium (24h), long (1 week)
#PBS -q {queue}
#PBS -j oe

source /etc/profile

echo "Running job $PBS_ARRAYID"

setupATLAS
lsetup root
python {runner} $PBS_ARRAYID

echo "Done"
