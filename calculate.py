import csv, random
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MAX={'C1':20,'C2':20,'C3':15,'C4':15,'C5':10,'C6':10,'C7':10}
with open(ROOT/'SCORE_MATRIX.csv',encoding='utf-8-sig') as f:
    rows=list(csv.DictReader(f))

def total(r):
    return sum(int(r[k]) for k in MAX)

for r in rows:
    assert total(r)==int(r['score']), (r['participant'], total(r), r['score'])

rows=sorted(rows,key=lambda r:(-total(r),-int(r['C2']),-int(r['C1']),-int(r['C4']),-int(r['C3']),r['participant']))
assert rows[0]['participant']=='Метод Лаб' and total(rows[0])==95

rng=random.Random(42)
lead=0
for _ in range(50000):
    w={k:MAX[k]*rng.uniform(0.8,1.2) for k in MAX}
    s=sum(w.values())
    w={k:v*100/s for k,v in w.items()}
    scored=[]
    for r in rows:
        value=sum((int(r[k])/MAX[k])*w[k] for k in MAX)
        scored.append((value,r))
    scored.sort(key=lambda t:(-t[0],-int(t[1]['C2']),-int(t[1]['C1']),-int(t[1]['C4']),-int(t[1]['C3']),t[1]['participant']))
    if scored[0][1]['participant']=='Метод Лаб':
        lead+=1

print('OK: score matrix sums and ranking verified')
print('Sensitivity: Метод Лаб first', lead, 'of 50000')
