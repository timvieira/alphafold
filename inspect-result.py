import pickle, pandas as pd, pylab as pl, numpy as np
from argparse import ArgumentParser
from pprint import pprint
from path import Path
from util import load

p = ArgumentParser()
p.add_argument('directory', type=Path)
args = p.parse_args()

config = load(args.directory / 'args.pkl')

pprint(config.__dict__)

df = pd.DataFrame(load(args.directory / 'log.pkl.bz2'))

p = load(args.directory / 'solution.pkl')

smoothing = 100

pl.figure()
pl.title('degree')
pl.plot(df.degree.ewm(smoothing).mean())

pl.figure()
pl.title('program length')
pl.plot(df['p_length'].ewm(smoothing).mean())

if config.search == 'mcts':
    pl.figure()
    pl.title('estimated cost')
    pl.plot((df['c'] / (1+df['n'])).ewm(smoothing).mean())

pl.show()

from IPython import embed; embed()
