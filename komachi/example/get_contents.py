# -*- coding: utf-8 -*-

import sys
import json
from komachi import parse_contents

url = sys.argv[1]
contents = parse_contents(url)
if len(sys.argv) == 2:
    name = contents['topic_id']
else:
    name = sys.argv[2]

with open('{}.json'.format(name), 'w') as f:
    json.dump(contents, f, indent=4, ensure_ascii=False)
