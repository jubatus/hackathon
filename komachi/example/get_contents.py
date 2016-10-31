# -*- coding: utf-8 -*-

import json
from komachi import parse_contents

# please edit 
url = 'http://komachi.yomiuri.co.jp/t/2016/1025/782664.htm?g=06'
contents = parse_contents(url)

with open('contents.json', 'w') as f:
    json.dump(contents, f, indent=4, ensure_ascii=False)
