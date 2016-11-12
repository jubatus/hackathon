# -*- coding: utf-8 -*-
import sys
import json
from komachi.komachi import parse_titles_in_day, parse_contents

# Usage:
# $ python get_contents_in_month.py 2014 10

def parse_contents_in_month(f, year, month):
    for day in range(1, 32):
        print('parse {}/{}/{}'.format(year, month, day))
        for page_id in range(1,5): # とりあえず5ページ目まで取得する
            try:
                titles = parse_titles_in_day(year, month, day, page_id)
                if len(titles) == 0: break
                for title in titles:
                    url = title['link']
                    contents = parse_contents(url)
                    if contents is not None:
                        f.write(json.dumps(contents, ensure_ascii=False))
                        f.write('\n')
            except Exception:
                break


if __name__ == '__main__':
    name = 'whole_contents.json'
    f = open(name, 'w')
    for year in range(2004, 2017, 1):
        for month in range(1, 13, 1):
            parse_contents_in_month(f, year, month)
    f.close()
