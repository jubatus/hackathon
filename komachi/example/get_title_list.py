# -*- coding: utf-8 -*-
import sys
import json
from komachi import parse_titles_in_group

group_id = sys.argv[1]
title_list = parse_titles_in_group(group_id)

with open('title_list_{}.json'.format(group_id), 'w') as f:
    json.dump(title_list, f, indent=4, ensure_ascii=False)
