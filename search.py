import pickle
from argparse import ArgumentParser
from path import Path

from arsenal import colors
from arsenal.maths import log_sample
from arsenal import timers

from dyna.dyna1.explore import exploration, Program, TransformedProgram, SimulatedAnnealing
from dyna.term import vars

from benchmarks import benchmark
from configurations import search_alg, search_graph
from util import load_program, dump


def main():
    p = ArgumentParser()
    p.add_argument('filenames', type=Path, help='benchmark to run', nargs='+')
    p.add_argument('--reps', type=int, required=True)
    p.add_argument('--search-depth', type=int, default=100)
    p.add_argument('--temperature', type=float, default=1.0)
    p.add_argument('--beam-size', type=int)
    p.add_argument('--force', action='store_true')
    p.add_argument('--dry', action='store_true')

    p.add_argument('--search', choices=search_alg, nargs='+', default=search_alg)
    p.add_argument('--graph', choices=search_graph, nargs='+', default=search_alg)

    p.add_argument('--interactive','-i', action='store_true')
    p.add_argument('--show-transforms', action='store_true')
    p.add_argument('--show-program', action='store_true')

    args = p.parse_args()

    for filename in args.filenames:
        print(colors.light.cyan % ('='*80))
        print(colors.light.cyan % f'Running {filename}')

        if filename.endswith('.run.pkl'):
            continue

        assert filename.endswith('.pkl'), 'use the pkl rather than the dyna file.'

        for graph in args.graph:
            for search in args.search:

                directory = filename + '.algs'
                if not directory.exists(): directory.mkdir()
                output_file = directory / f'{search}-{graph}.pkl'

                print(colors.cyan % f'Running {output_file}')

                if not args.dry and not args.force and output_file.exists():
                    print('path already exists')
                    try:
                        load_program(output_file, benchmark)
                    except EOFError:
                        print(colors.light.cyan % f'Previous file had an error: {output_file}')
                        pass
                    else:
                        continue

                B = filename.dirname().basename()
                if B not in benchmark:
                    print(colors.light.red % f'skipping {B}')
                    continue
                b = benchmark[B]

                p = load_program(filename, b)
                G = search_graph[graph](p, args)
                S = search_alg[search](G = G,
                                       benchmark = b,
                                       program = p,
                                       args = args,
                                       checkpoint = None)
                s = S.best

#                print('running benchmark...')
#                b(s, 1)
#                print(colors.ok)
#                print(s)

                if not args.dry:
                    try:
                        dump(s, output_file)
                    except Exception as e:
                        print(colors.light.red % f'Error writing pickle: {e}')
                        output_file.unlink()
                        s.parent = None         # try again
                        dump(s, output_file)
                    print('wrote', output_file)
                    dump(S.log, output_file + '.log')

                if args.show_transforms:
                    s.show_transforms()
                if args.show_program:
                    print(s)
                if args.interactive:
                    from IPython import embed; embed()


if __name__ == '__main__':
    main()
