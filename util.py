import bz2
import pickle
from path import Path
from dyna.dyna1 import Program


def load_program(filename, bench):
    if Path(filename).endswith('.pkl'):
        with open(filename, 'rb') as f:
            p = pickle.load(f)
    elif filename.endswith('.dyna'):
        p = Program(open(filename).read(), bench.inputs, bench.outputs)
    else:
        raise ValueError(f'unrecognized file type: {filename}')
    assert isinstance(p, Program), [filename, p]
    return p


def dump(obj, x):
    if x.endswith('.bz2') or x.endswith('.bz2~'):
        with bz2.BZ2File(x, 'wb') as f:
            return pickle.dump(obj, f)
    pickle.dump(obj, open(x, 'wb'))


def load(x):
    if x.endswith('.bz2') or x.endswith('.bz2~'):
        with bz2.BZ2File(x, 'rb') as f:
            return pickle.load(f)
    return pickle.load(open(x, 'rb'))
