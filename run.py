import pickle
import numpy as np
from arsenal import colors
from arsenal.maths import log_sample
from path import Path
from dyna.dyna1 import Program
from argparse import ArgumentParser
from benchmarks import benchmark
from util import load

p = ArgumentParser()

p.add_argument('filenames', type=Path, nargs='+')
p.add_argument('--force', action='store_true')

args = p.parse_args()


for f in args.filenames:
    if f.endswith('.run.pkl'):
        continue

    B = f.dirname() / 'args.pkl'
    b = load(B).benchmark if B.exists() else f.dirname().basename()

    opts = load(B)
#    if opts.graph.startswith('macro'): continue

    if b not in benchmark:
        print('skipping benchmark', b)
        continue
    bench = benchmark[b]

    print(colors.cyan % ('='*80))
    print(colors.cyan % f'Running {f}')

    output_file = f + '.run.pkl'

    if not args.force and output_file.exists():
        print('path already exists')
        continue

    if f.endswith('.dyna'):
        p = Program(open(f).read(), bench.inputs, bench.outputs)

    elif f.endswith('.run.pkl'):
        continue

    elif f.endswith('.pkl'):
        p = load(f)

    else:
        raise ValueError(f'unrecognized file type: {f}')

    assert isinstance(p, Program), p

#    try:
    output = bench(p, 1)    # not all benchmarks have test method, those that don't return {}
#    except AssertionError:
#        continue

    if output.pop('d', None) is None:
        print(colors.light.red % 'empty benchmark', opts.benchmark)

    print(output)
    print(colors.yellow % f'wrote {output_file}')

    with open(output_file, 'wb') as f:
        pickle.dump(output, f)
