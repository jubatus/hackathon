# -*- coding: utf-8 -*-
import sys
from komachi.kit import KomachiLoader, get_schema_for_recommender
from jubakit.recommender import Schema, Dataset, Config, Recommender

def main():
    # parser で取得した json ファイルを入力します
    path = sys.argv[1]
    
    # json ファイルを読み込むローダーを作成します
    loader = KomachiLoader(path, include_responses=False, include_votes=False)

    # Jubatusに投入するDatasetのインスタンスを作成します
    # スキーマは komachi.kit に記載のあるデフォルトのものを利用します
    dataset = Dataset(loader, get_schema_for_recommender())

    # Recommenderサーバを起動します
    recommender = Recommender.run(Config(method='inverted_index'))
    
    # Recommenderにデータを登録します
    id2record = {}
    for (idx, row_id, success) in recommender.update_row(dataset):
        id2record[row_id] = dataset.get(idx)

    # Recommenderでレコメンドを行います。
    for (idx, row_id, result) in recommender.similar_row_from_id(dataset):
        # 類似度の高いレコードをn_records件取得します
        n_records = 5
        top_ids = []
        top_scores = []
        for i in range(len(result)):
            if result[i].id == row_id: continue
            top_ids.append(result[i].id)
            top_scores.append(result[i].score)
            if i > n_records: break

        # レコメンド結果と記事を表示します
        if len(top_ids) == 0:
            print('記事 {0} と似ている記事は見つかりませんでした'.format(row_id))
            print('\t{0} => {1}'.format(row_id, id2record[row_id]['title']))
        else:
            print('記事 {0} と似ている記事が見つかりました！'.format(row_id))
            print('\t{0} (類似度:{1:.3f}) : {2}'.format(row_id, 1.0, id2record[row_id]['title']))
            for top_id, top_score in zip(top_ids, top_scores):
                print('\t{0} (類似度:{1:.3f}) : {2}'.format(top_id, top_score, id2record[top_id]['title']))
        print()

if __name__ == '__main__':
    main()
