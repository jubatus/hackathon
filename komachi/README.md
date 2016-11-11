# komachi

komachi は読売新聞社より提供されている[発言小町](http://komachi.yomiuri.co.jp/)のトピックスを収集し、`json`形式で出力するスクリプトです。

## インストール

```
$ git clone https://github.com/jubatus/hackathon.git
$ cd hackathon/komachi
$ python setup.py install
```

## 依存パッケージ

* Python 2.6, 2.7, 3.3, 3.4 or 3.5
* [Beafutiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc)
* [lxml](http://lxml.de/)

## ジャンル一覧

発言小町の以下のジャンルの投稿を取得することができます。

| ID | ジャンル名 |
|:--:|:------------|
| 00 | 全ジャンル一覧 | 
| 01 | 生活・身近な話題 | 
| 02 | 恋愛・結婚・離婚 | 
| 03 | 妊娠・出産・育児 | 
| 04 | キャリア・職場 | 
| 05 | 家族・友人・人間関係 | 
| 06 | 心や体の悩み | 
| 07 | 美容・ファッション・ダイエット | 
| 08 | 趣味・教育・教養 | 
| 09 | 旅行・国内外の地域情報 | 
| 10 | 男性から発信するトピ | 
| 11 | 編集部からのトピ | 
| 15 | 弁護士に相談するトピ |

各ジャンルから最新の1000件の投稿を取得することができます。

ページID (1~10)を指定することで、100件ずつ投稿を取得することも可能です。

## 使い方

### 特定の投稿の内容を取得する

以下のスクリプトを実行することにより、URLで指定した特定の投稿を取得することができます。
第一引数にURLを、第二引数にファイル名（任意）を入力してください。

```
$ python get_contents.py http://komachi.yomiuri.co.jp/t/2016/mmdd/******.htm?g=** sample
```

```python:get_contents.py

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

```

```json:contents.json
{
    "topic_id",                 # トピックID
    "user_name": "USERNAME",    # ユーザ名
    "user_id": "USER ID",       # ユーザID
    "title": "TITLE",           # 投稿のタイトル
    "message": "MESSAGE",       # 投稿本文
    "n_response": "0"           # レス数
    "responses": [],            # レス本文
    "group": "GROUP",           # ジャンル
    "date": "2016年m月d日 H:M",  # 投稿日・時間
    "n_favorite": "0",          # お気に入りの数
    "face": "kao***",           # 感情アイコンID
    "votes": [],                # 得票数
    "url": "http://komachi.yomiuri.co.jp/t/2016/mmdd/******.htm?g=**",
}
```

### ジャンル配下の投稿リストを取得する

以下のスクリプトを実行することにより、指定したジャンル配下にある投稿リストをすべて取得することができます。
出力ファイル(`contents_**.json`)の各行にjson形式で投稿が記載されます。
第一引数にジャンルコードを入力してください。

```
$ python get_contents_in_group.py 00
```

```
import sys
import json
from komachi import parse_titles_in_group, parse_contents

group_id = sys.argv[1]

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
```

```json:contents_list.json
[
    {
        "link": "http://komachi.yomiuri.co.jp/t/2016/mmdd/******.htm?g=**",
        "title": "TITLE",	        # 投稿のタイトル
        "n_response": "0",          # レス数
        "n_favorite": "1",          # お気に入り数
        "date": "8月18日 22:57",     # 投稿日・時間
        "rank": "761",              # アクセスランキング（ランク外は-1)
        "group": "全ジャンル一覧"      # ジャンル名
    },
    {
        "link": "http://komachi.yomiuri.co.jp/t/2016/mmdd/******.htm?g=**",
        ...
    },
    ...
]
```

### 取得可能なすべての投稿を取得する

以下のスクリプトを実行することにより、掲載中のすべての投稿、およびその内容を取得することができます。
出力ファイル(`all.json`)の各行にjson形式で投稿が記載されます。
ダウンロードに時間がかかるのでご注意ください。

``` python:get_all.py

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


```

## LICENSE

MIT License
