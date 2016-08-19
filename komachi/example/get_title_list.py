# -*- coding: utf-8 -*-
import json
from komachi import parse_titles_in_group

group_id = '00' 
title_list = parse_titles_in_group(group_id)

with open('title_list.json', 'w') as f:
    json.dump(title_list, f, indent=4, ensure_ascii=False)
