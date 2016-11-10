# -*- coding: utf-8 -*-

import json
from komachi import parse_titles_in_group, parse_contents

group_id = '00'

path = 'contents_{}.json'.format(group_id)
f = open(path, 'w')

result = []
titles = parse_titles_in_group(group_id)
for title in titles:
    url = title['link']
    contents = parse_contents(url)
    if contents is not None:
        f.write(json.dumps(contents, ensure_ascii=False))
        f.write('\n')

f.close()
