import sys
import json
import random
from datetime import datetime

def log(s):
    print >> sys.stderr, "%s > %s" % (datetime.now().isoformat(), s)

probability = float(sys.argv[1])

log('Sampling %0.2f%% of lines' % (100 * probability))

lineno = 0
sampled = 0
for line in sys.stdin:
    lineno += 1
    if random.random() < probability:
        sampled += 1
        sys.stdout.write(line)

log('Selected %d lines out of %d (%0.2f%%)' % (sampled, lineno, 100 * float(sampled) / lineno))
