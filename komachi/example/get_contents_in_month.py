# -*- coding: utf-8 -*-
import sys
import json
from komachi.komachi import parse_titles_in_day, parse_contents

# Usage:
# $ python get_contents_in_month.py 2014 10

def parse_contents_in_month(f, year, month):
    for day in range(1, 32):
        for page_id in range(1,5): # とりあえず5ページ目まで取得する
            titles = parse_titles_in_day(year, month, day, page_id)
            if len(titles) == 0: break
            for title in titles:
                url = title['link']
                contents = parse_contents(url)
                if contents is not None:
                    f.write(json.dumps(contents, ensure_ascii=False))
                    f.write('\n')

if __name__ == '__main__':
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    name = '{}{}.json'.format(year, month)
    f = open(name, 'w')
    parse_contents_in_month(f, year, month)
    f.close()
