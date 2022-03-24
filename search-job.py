import os, pickle
from argparse import ArgumentParser
from path import Path

from arsenal import colors

from benchmarks import benchmark
from configurations import search_alg, search_graph
from util import load_program, dump


def main():
    p = ArgumentParser()
    p.add_argument('benchmark', choices=benchmark)
    p.add_argument('filename', type=Path)
    p.add_argument('--results', type=Path, required=True)
    p.add_argument('--force', action='store_true')

    p.add_argument('--reps', type=int, required=True)
    p.add_argument('--temperature', type=float, default=1.0)
    p.add_argument('--beam-size', type=int)
    p.add_argument('--search-depth', type=int, required=True)

    p.add_argument('--search', choices=search_alg, required=True)
    p.add_argument('--graph', choices=search_graph, required=True)

    args = p.parse_args()

    filename = args.filename

    os.makedirs(args.results, exist_ok=True)

    print(colors.light.cyan % ('='*80))
    print(colors.light.cyan % f'Running {filename}')

    assert filename.endswith('.pkl'), 'use the pkl rather than the dyna file.'

    output_file = args.results / 'solution.pkl'
    print(colors.cyan % f'Running {output_file}')

    # save the CLI arguments
    dump(args, args.results / 'args.pkl')

    if not args.force and output_file.exists():
        print('path already exists')
        try:
            load_program(output_file, benchmark)
        except EOFError:
            print(colors.light.cyan % f'Previous file had an error: {output_file}')
            pass
        else:
            return

    # XXX: a job might die mid check point.
    def checkpoint(alg):
        dump(alg.log, args.results / 'log.pkl.bz2~')

        s = alg.best
        dump(s, output_file + '~')

        # rename after
        (args.results / 'log.pkl.bz2~').rename(args.results / 'log.pkl.bz2')
        (output_file + '~').rename(output_file)

        print(colors.magenta % f'checkpoint {args.results}')

    bench = benchmark[args.benchmark]

    p = load_program(filename, bench)

    G = search_graph[args.graph](p, args)
    S = search_alg[args.search](G = G, benchmark = bench, program = p, args = args,
                                checkpoint = checkpoint)
    s = S.best

    print(
        'optimal degree:', bench.optimal,
        'initial degree:', p.degree,
        'recover degree:', (colors.light.green if s.degree <= bench.optimal else colors.yellow) % s.degree,
    )

    checkpoint(S)


if __name__ == '__main__':
    main()
