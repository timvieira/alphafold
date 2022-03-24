import bz2
from path import Path
from arsenal import iterview


finished = []
for x in Path('results-5b').glob('*/log.pkl'):
    # XXX: only bother converting completed jobs
    if not (x.dirname() / 'finish').exists(): continue
    finished.append(x)

print('finished', len(finished))
    
for x in iterview(finished):
    with open(x, 'rb') as f, bz2.BZ2File(x + '.bz2', 'wb') as g:
        g.write(f.read())
    x.unlink()  # delete the old file
