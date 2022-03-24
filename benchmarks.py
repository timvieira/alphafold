from dyna.benchmarks.benchmark import Benchmark
from dyna.benchmarks.cky import CKY as CKY3, CKY4, CKY5, CKY0
from dyna.benchmarks.chain import Chain, ChainRisk
from dyna.benchmarks.dep.split_head import SplitHead
from dyna.benchmarks.dep.bilexical import BilexicalLabeled, BilexicalUnlabeled
from dyna.benchmarks.edit import EditDistance
from dyna.benchmarks.itg import ITG
from dyna.benchmarks.BarHillel import BarHillel
from dyna.benchmarks.paths import PathSumSE, SemiMarkov, SingleSourceFromAllPairs
#from dyna.benchmarks.lig import LIG
from dyna.benchmarks.hmm import HMM


benchmark = {}
#benchmark['chain-05'] = Chain( 5)
benchmark['chain-10'] = Chain(10)
#benchmark['chain-15'] = Chain(15)
benchmark['chain-20'] = Chain(20)

benchmark['chain-risk'] = ChainRisk()

benchmark['cky0'] = CKY0()
benchmark['cky3'] = CKY3()
benchmark['cky4'] = CKY4()
#benchmark['cky5'] = CKY5()

benchmark['bilexical-labeled'] = BilexicalLabeled()
benchmark['bilexical-unlabeled'] = BilexicalUnlabeled()

benchmark['edit'] = EditDistance()

benchmark['bar-hillel'] = BarHillel()

benchmark['itg'] = ITG()

benchmark['hmm'] = HMM()

#benchmark['lig'] = LIG()

benchmark['split-head'] = SplitHead()

benchmark['semi-markov'] = SemiMarkov()

if 0: benchmark['trace-mm'] = Benchmark(
    src = """
    % trace of mat-mul
    c(I,K) += a(I,J) * b(J,K).
    goal += c(I,I).
    """,
    inputs = 'a(_,_). b(_,_).',
    outputs = 'goal.',
    optimal = 2,
    annotations = None,
    load = None,
    check = None,
)


# TODO:
benchmark['path-sum-se'] = PathSumSE()

#benchmark['not-allpairs'] = SingleSourceFromAllPairs()



if __name__ == '__main__':
    from arsenal import colors

    for x in benchmark:
        print()
        print(colors.green % '==================================================')
        print(x)
        b = benchmark[x]
        print(benchmark[x].user_src)
        print(f'Degree {b.src.degree}, Optimal: {b.optimal}')
