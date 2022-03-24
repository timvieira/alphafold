#import sys; sys.path.append('.')
import os
import numpy as np
import subprocess
from path import Path
from arsenal import colors
from experiments.benchmarks import benchmark
from datetime import datetime
from hashlib import sha1

root = Path('stress-tests')
#results = Path('results-3b')
results = Path('results-5b')


def sge(name, cmd):
    print(colors.green % cmd)

    cmd = cmd.strip()

    date = datetime.now().strftime("%Y-%m-%d")
    out = results / ('%s-%s-%s' % (date, name, sha1(cmd.encode('utf-8')).hexdigest()))

    print(colors.green % f'==> {out}')

#    if out.exists() and not args.force:
#        print()
#        print("[warning] skipping dump already exists.")
#        print()
#        return

    os.makedirs(out, exist_ok=True)

    qsub = ['qsub']

    sge_cmd = qsub + ['-cwd',
         '-j', 'yes',
         '-o', out / 'stdout.txt',      # stdout goes here.
         '-b', 'yes',
         '-N', name,               # job name
         '-l', "arch=*64*,mem_free=6G,ram_free=6G",  # flags for job requirements
         '-q', "all.q@c*.clsp.jhu.edu", # run on c nodes
         '/bin/bash',
         './my-sge-wrapper',            # use wrapper script which has boilerplate for tracking jobid, starttime, etc.
         out,
         cmd + f' --results {out}',      # pass in the --results directory as an argument
    ]

    with open(out / 'cmd.txt', 'w') as f:
        f.write(cmd + f' --results {out}')

    print(' '.join(map(str, sge_cmd)))
    if 1:
        output = subprocess.check_output(list(map(str, sge_cmd))).decode('utf-8')
        print(output)

        # write SGE's response to a file in the results directory.  It will contain the jobid.
        with open(out / 'submit.txt', 'w') as f:
            f.write(output)

#    print("<<<<<STOPPING AFTER JUST ONE FOR TESTING>>>>>>")
#    exit()


def main():

    opts = '--reps 500_000 --search-depth 100 --force'

    cmds = []
    for size in [
#            '3',
#            '4',
            '5',
    ]:
        for b in benchmark:
            for instance in (root / size / b).glob('*.pkl'):
                for search in [
                        'beam --beam-size 100',
                        'beam --beam-size 1000',
                        'mcts',
                ]:
                    for graph in ['basic1', 'basic2', 'macro2']:
                        assert instance.exists()
                        cmd = f'python -u experiments/search-job.py {b} {instance} --search {search} --graph {graph} {opts}'
                        cmds.append(cmd)

    np.random.shuffle(cmds)
    for cmd in cmds:
        sge('j5', cmd)


if __name__ == '__main__':
    main()
