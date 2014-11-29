import json
import sys

g = json.load(sys.stdin)
print(g['ClusterId'])

