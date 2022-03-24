import os
from path import Path
import pickle, numpy as np

from arsenal import colors, iterview

from dyna.dyna1 import Program
from dyna.frontend.pretty import pp


FAILED = []

def generate_data(name, bench, args):

    rd = args.results / name

    if not args.force and rd.exists():
        print(colors.light.red % f'skipping existing directory: {rd}')
        return

    os.system(f'rm -rf {rd}')
    os.system(f'mkdir -p {rd}')

    print(colors.light.cyan % 'Generating random transforms...', end=' ')
    E = generating_random_transforms(bench, args)
    print(colors.light.cyan % 'done')

    if len(E) < args.inits:
        print(colors.light.red % ('*'*120))
        print(colors.light.red % 'failed to create data')
        print(colors.light.red % ('*'*120))
        #raise ValueError('failed to create data')
        FAILED.append(name)

    for i, x in enumerate(E):
        x.save(f'{rd}/{i:02d}.dyna')

        # this version stores the transforms
        with open(f'{rd}/{i:02d}.pkl', 'wb') as f:
            pickle.dump(x, f)

        #print('=========================================================')
#        x.show_transforms()
        #from dyna.dyna1.search_fold import search_binarize
        #y = search_binarize(x, 1000, verbose=True)
        #print(y)
        #print(x.degree, '==>', y.degree)
        #print(x.degree_lb(), '==>', y.degree_lb())
        #print('optimal:', bench.optimal)

    print(colors.light.yellow % f'wrote benchmark directory: {rd}')




from dyna.dyna1.explore.graph1 import Graph1
from dyna.dyna1.explore.swor import SWOR
def generating_random_transforms(benchmark, args):

    program = benchmark.src
    G = Graph1(
        src = program,
        max_depth = args.generate_depth,
        #TRANSFORMS = ['unfold', 'elim', 'fold'],
        TRANSFORMS = ['unfold', 'fold'],
    )

    S = SWOR(
        G = G,
        program = program,
        benchmark = benchmark,
        reps = 0,
        ORACLE_STOP = False,
        checkpoint = None,
    )

    survivors = []
    try:
        for _ in range(10_000):

            S.reps = 100000000
            s = S._run()
            x = s.program

            if x.greedy_binarize().degree <= benchmark.optimal:
                continue

            if 1:
                #print()
                #print()
                #print(x)
                x.show_transforms()

            survivors.append(x)
            print(colors.light.yellow % f'found {len(survivors)}')
            if len(survivors) >= args.inits:
                 break

    except KeyboardInterrupt:
        print('^C')

    return survivors


def main():
    from benchmarks import benchmark
    from argparse import ArgumentParser

    p = ArgumentParser()
    p.add_argument('--names', choices=list(benchmark), nargs='*',
                   default=benchmark,
                   help='list of benchmarks to run')
    p.add_argument('--generate-depth', type=int, required=True)
    p.add_argument('--results', type=Path, required=True)
    p.add_argument('--force', action='store_true')
    p.add_argument('--inits', type=int, required=True)
    args = p.parse_args()

    for name in args.names:
        print()
        print(colors.cyan % ('='*120))
        print(colors.cyan % f'Running {name}')
        generate_data(name, benchmark[name], args)


    if FAILED:
        print()
        print(colors.light.red % '*** The folling datasets failed ***')
        for x in FAILED:
            print(colors.light.red % x)


if __name__ == '__main__':
    main()
