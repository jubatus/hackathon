# -*- coding: utf-8 -*-

import json
from komachi import parse_title_page, parse_contents

group_id = '00'
page_id = 1

result = []
titles = parse_title_page(group_id, page_id)
for i, title in enumerate(titles):
    url = title['link']
    ret = parse_contents(url)
    if ret is not None:
        result.append(ret)

with open('contents_list.json', 'w') as outfile:
    json.dump(result, outfile, indent=4, ensure_ascii=False)
