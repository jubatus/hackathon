# -*- coding:utf-8 -*-
from jubatus.recommender.client import Recommender
from jubatus.common import Datum
import argparse
import json
import os

def train_jubatus(cl, args):
    '''
    jubatusクライアントに各トピックを学習させる
    サンプルでは本文のみをDatumに格納し学習させている
    同時にtopic_idをキーとして、タイトルと本文を格納する辞書を作成する
    '''
    topic_dict = {}
    with open(args.input_file) as f:
        for line in f:
            j = json.loads(line)
            topic_id = j["topic_id"]     # トピックID
            user_name = j["user_name"]   # 投稿者名
            user_id = j["user_id"]       # 投稿者ID
            title = j["title"]           # 投稿タイトル
            message = j["message"]       # 投稿本文
            n_response = j["n_response"] # レス数
            responses = j["responses"]   # レス本文
            group = j["group"]           # ジャンル
            date = j["date"]             # 投稿日・時間
            n_favorite = j["n_favorite"] # お気に入りの数
            face = j["face"]             # 感情アイコンID
            votes = j["votes"]           # 得票数
            url = j["url"]
        
            d = Datum()
            d.add_string("message", message)
            cl.update_row(topic_id, d)
            topic_dict[topic_id] = {"title": title, "message": message}

    return topic_dict

def write_header(f,title):
    f.write("<head>\n")
    f.write('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n')
    f.write('<title>{}</title>\n'.format(title))
    f.write('</head>\n')

def print_html(cl, topic_dict):
    '''
    近傍探索を行った結果をhtmlに書き出す
    htmlファイルはtopic idごとに作成され、タイトル・本文と類似する記事10件が書き込まれる
    '''
    for topic in topic_dict:
        with open(os.path.join("html",topic)+".html", "w") as f:
            neighbors = cl.similar_row_from_id(topic, 10)
            f.write("<html>")
            write_header(f, topic_dict[topic]["title"])
            f.write("<body>")
            f.write('<div id="title" style="width 500px;">タイトル：{}</div><br>'.format(topic_dict[topic]["title"]))
            f.write('<div id="message" style="width: 500px;">{}</div>'.format(topic_dict[topic]["message"]))
            f.write('<div id="neighbors" style="position:relative;">')
            f.write('<table>')
            f.write('<tr><th>類似度</th><th>トピックタイトル</th></tr><br>')
            for neighbor in neighbors[1:]:
                f.write('<tr><td> 類似度:{:.4f}</td><td><a href="{}.html">{}</a></td></tr><br>'.format(neighbor.score, neighbor.id, topic_dict[neighbor.id]["title"]))
            f.write('</table>')
            f.write('</div>')
            f.write("</body>")
            f.write("</html>")

def make_client():
    return Recommender("localhost", 9199, "hoge", 0)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", action="store", dest = "input_file", required=True, help="入力のjsonファイル")
    return parser.parse_args()

def run():
    args = parse_args()
    cl = make_client()
    topic_dict = train_jubatus(cl, args)
    print_html(cl, topic_dict)

if __name__ == "__main__":
    '''
    使い方：
      1. jubatusの起動
      jubarecommender -f config/recommender.conf &
      2. scriptの起動
      python recommender_example.py -f all.json
      3. ブラウザで適当なファイルを開く
    '''

    try:
        os.mkdir("html")
    except FileExistsError:
        pass
    run()

