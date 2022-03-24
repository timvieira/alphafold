#_______________________________________________________________________________
# SEARCH GRAPHS
# - TWO types of state spaces Graph1 and Graph2
# - two types of action space macro and basic
from dyna.dyna1.program import degrees
from dyna.dyna1.explore.graph1 import Graph1
from dyna.dyna1.explore.graph2 import Graph2

def basic1(p, args):
    return Graph1(
        src = p,
        max_depth = args.search_depth,
        TRANSFORMS = ['unfold', 'elim', 'fold'],
        cost = degrees,
    )

def macro1(p, args):
    return Graph1(
        src = p,
        max_depth = args.search_depth,
        TRANSFORMS = ['unfold', 'elim', 'fold*'],
        cost = degrees,
    )

def basic2(p, args):
    return Graph2(
        src = p,
        max_depth = args.search_depth,
        TRANSFORMS = ['unfold', 'elim', 'fold'],
        cost = degrees,
    )

def macro2(p, args):
    return Graph2(
        src = p,
        max_depth = args.search_depth,
        TRANSFORMS = ['unfold', 'elim', 'fold*'],
        cost = degrees,
    )

def basic3(p, args):
    return Graph2(
        src = p,
        max_depth = args.search_depth,
        TRANSFORMS = ['unfold', 'elim', 'fold', 'anti_fold'],
        cost = degrees,
    )


search_graph = {
    'basic1': basic1,
    'basic2': basic2,
    'basic3': basic3,    # XXX: anti-fold
    'macro1': macro1,
    'macro2': macro2,
}

#_______________________________________________________________________________
# SEARCH ALGORITHMS

from dyna.dyna1.explore.annealing import SimulatedAnnealing
from dyna.dyna1.explore.beam import BeamSearch
from dyna.dyna1.explore.mcts import MCTS
from dyna.dyna1.explore.swor import SWOR

def anneal(G, benchmark, program, args, checkpoint):  # graph is ignored.
    return SimulatedAnnealing(
        G = G,
        benchmark = benchmark,
        program = program,
        reps = args.reps,
        temperature = args.temperature,
        ORACLE_STOP = True,
        checkpoint = checkpoint,
    )

def beam(G, benchmark, program, args, checkpoint):
    return BeamSearch(
        G = G,
        program = program,
        benchmark = benchmark,
        reps = args.reps,
        beam_size = args.beam_size,
        ORACLE_STOP = True,
        checkpoint = checkpoint,
    )

def mcts(G, benchmark, program, args, checkpoint):
    return MCTS(
        G = G,
        program = program,
        benchmark = benchmark,
        reps = args.reps,
        ORACLE_STOP = True,
        checkpoint = checkpoint,
    )

def swor(G, benchmark, program, args, checkpoint):
    return SWOR(
        G = G,
        program = program,
        benchmark = benchmark,
        reps = args.reps,
        ORACLE_STOP = True,
        checkpoint = checkpoint,
    )


search_alg = {
    'anneal': anneal,
    'mcts':   mcts,
    'swor':   swor,
    'beam':   beam,
}

#_______________________________________________________________________________
#
