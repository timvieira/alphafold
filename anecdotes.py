"""
How well do we recover the optimal variant of several classical NLP algorithms?
"""
import numpy as np
from arsenal import colors
from argparse import ArgumentParser

from benchmarks import benchmark
from configurations import search_alg, search_graph


results = []
def check_optimal(x, b, s):
    if b.optimal != s.degree:
        print('opt-degree:', x, colors.light.yellow % f'subopt: want {b.optimal}, have: {s.degree}')
    else:
        print('opt-degree:', x, colors.light.green % f'optimal! {b.optimal}')
    results.append((x, b.optimal, s.degree))
    #e.best.show_transforms()


def main():
    p = ArgumentParser()
    p.add_argument('filters', nargs='*')
    p.add_argument('--skip', nargs='*')
    p.add_argument('--check', action='store_true')
    p.add_argument('--reps', type=int, default=10_000)
    p.add_argument('--beam-size', type=int)
    p.add_argument('--search-depth', type=int, default=100)
    p.add_argument('--temperature', type=float, default=1.0)
    p.add_argument('--search', choices=search_alg, required=True)
    p.add_argument('--graph', choices=search_graph, required=True)
    args = p.parse_args()


    filters = list(args.filters) if args.filters else ['']
    skip = list(args.skip) if args.skip else []
    for kw in filters:
        kw = kw.lower()
        for name in sorted(benchmark):
            if ((kw in name) and not any((z in name) for z in skip)):

                b = benchmark[name]
                p = b.src
                print()
                print()
                print(colors.yellow % ('='*100))
                print(colors.yellow % name)
                print(p)
                print()

                G = search_graph[args.graph](p, args)
                S = search_alg[args.search](G = G,
                                            benchmark = b,
                                            program = p,
                                            args = args,
                                            checkpoint = None)
                s = S.best

                check_optimal(name, b, s)

                if args.check:
                    print(colors.yellow % 'testing...', end=' ')
                    out = p(s, 1)
                    assert out == {} or not out['fail'], out
                    print(colors.ok)

                s.show_transforms()

    print()
    print('RESULTS')
    print('=======')
    for x, want, have in results:
        print(x, (colors.light.green % want) if want == have else
              (f'have = {colors.light.red % have}, want = {want}'))
    print()

if __name__ == '__main__':
    main()
