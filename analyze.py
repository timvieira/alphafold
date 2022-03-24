import re, pickle, numpy as np
import pandas as pd
from dyna.dyna1 import Program
from path import Path
from argparse import ArgumentParser
from arsenal import colors, iterview

from benchmarks import benchmark
from search import search_alg
from util import load_program


p = ArgumentParser()
p.add_argument('--results', type=Path, required=True)
p.add_argument('--benchmarks', nargs='*', default=benchmark)
p.add_argument('--algs', nargs='*', default=search_alg)
args = p.parse_args()


data = []
for name in iterview(args.benchmarks):

#    print()
#    print(colors.light.green % name)

    bench = benchmark[name]

    for filename in sorted((args.results / name).glob('*.pkl')):

        if filename.endswith('.run.pkl'): continue

        p = load_program(filename, bench)

        item = dict(
            name = name,
            filename = filename,
            start_degree = p.degree,
            optimal_degree = bench.optimal
        )

        for x in args.algs:

            degree = np.nan

            out = (filename + '.algs') / (x + '.pkl')
            if out.exists():
                try:
                    s = load_program(out, bench)
                    degree = s.degree
                except EOFError as e:
                    print(colors.light.red % f'EOF Error {e}: {out}')

            item.update({x: degree, f'opt_{x}': (degree==bench.optimal)})

        #print(item)
        data.append(item)

#    p_value = verbose_paired_perm_test(df.fold, df.unfold)
#
#    data.append(dict(
#        name = d.basename(),
#        f = np.mean(df.fold),
#        u = np.mean(df.unfold),
#        opt = bench.optimal,
#        p = p_value,
#        success = np.mean(df.unfold == bench.optimal),
#    ))
#
#i = allfailed[0]
#print(exp.E[i])
#print(exp.F[i].best)
#print(exp.U[i].best)

df = pd.DataFrame(data)
df.to_csv('results.csv')

print()
print(colors.yellow % '==================================================')
print(colors.yellow % 'RESULTS:')
pd.set_option("precision", 2)
print(df)
print()

cols = [f'opt_{x}' for x in args.algs]
unsolved = ~df[cols[0]]
for c in cols:
    unsolved &= ~df[c]
print(colors.yellow % '\n== Unsolved ============================')
print(df[unsolved].filename)

print(colors.yellow % '\n== Info ============================')
print(df.groupby('name').mean()[['optimal_degree', 'start_degree']])

print(colors.yellow % '\n== Degree ============================')
print(df.groupby('name').mean()[[x for x in args.algs]])

print(colors.yellow % '\n== Optimality ============================')
print(df.groupby('name').mean()[[f'opt_{x}' for x in args.algs]])

print(colors.yellow % '\nOptimality Overall')
print(df.groupby('name').mean()[[f'opt_{x}' for x in args.algs]].mean())


#from IPython import embed; embed()

#print(colors.magenta % '==================================================')
#print(colors.magenta % 'LATEX:')
#print(colors.magenta % df.to_latex())


#from IPython import embed; embed()
