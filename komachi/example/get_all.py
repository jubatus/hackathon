# -*- coding: utf-8 -*-
import json
from komachi import parse_titles, parse_contents, parse_titles_in_group, GROUPS

path = "all.json"
f = open(path, 'w')

for group_id, group_name in GROUPS.items():
    titles = parse_titles_in_group(group_id)
    for title in titles:
        url = title['link']
        contents = parse_contents(url)
        if contents is not None:
            f.write(json.dumps(contents, ensure_ascii=False))
            f.write('\n')

f.close()
