# -*- coding: utf-8 -*-

import json
from komachi import parse_titles, parse_contents


result = dict()
titles = parse_titles()
for group_name, titles in titles.items():
    result[group_name] = []
    for title in titles:
        url = title['link']
        ret = parse_contents(url)
        if ret is not None:
            result[group_name].append(ret)

with open('all.json', 'w') as outfile:
    json.dump(result, outfile, indent=4, ensure_ascii=False)
