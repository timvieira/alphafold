#!/usr/bin/env python

# http://wiki.clsp.jhu.edu/view/Grid

import os, subprocess
from datetime import datetime
from hashlib import sha1
from argparse import ArgumentParser
from arsenal import colors
from path import Path
green = colors.green


# My export directory
# /export/c12/timv

p = ArgumentParser()
p.add_argument('--name', required=True)
p.add_argument('--job-file', type=Path, required=True)
p.add_argument('--dry', action='store_true')
p.add_argument('--force', action='store_true')

p.add_argument('--directory', type=Path, required=True)


args = p.parse_args()

NAME = args.name


for cmd in open(args.job_file):

    print(green % '==> %s <==' % cmd)

    cmd = cmd.strip()

    date = datetime.now().strftime("%Y-%m-%d")
    out = Path(args.directory / '%s-%s-%s' % (date, NAME, sha1(cmd.encode('utf-8')).hexdigest()))

    if out.exists() and not args.force:
        print()
        print("[warning] skipping dump already exists.")
        print()
        continue

    os.makedirs(out, exist_ok=True)

    if args.dry:
        qsub = ['echo', '-e', '"\n\033[1;31m$ fake-qsub\033[0m']
    else:
        qsub = ['qsub']

    sge_cmd = qsub + ['-cwd',
         '-j', 'yes',
         '-o', out / 'stdout.txt',      # stdout goes here.
         '-b', 'yes',
         '-N', args.name,               # job name
         '-l', "arch=*64*,mem_free=6G,ram_free=6G",  # flags for job requirements
         '-q', "all.q@c*.clsp.jhu.edu", # run on c nodes
         '/bin/bash',
         './my-sge-wrapper',            # use wrapper script which has boilerplate for tracking jobid, starttime, etc.
         out,
         cmd + f' --results {out}',      # pass in the --results directory as an argument
    ]

    #print ' '.join(map(str, sge_cmd))
    print(subprocess.check_output(list(map(str, sge_cmd))).decode('utf-8'))
