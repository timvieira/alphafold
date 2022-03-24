"""
Print out the command-line arguments to a job
"""
from argparse import ArgumentParser
from experiments.util import dump
from experiments.configurations import *
from experiments.benchmarks import *
from path import Path

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


dump(args, args.results / 'args.pkl')
