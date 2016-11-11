# -*- coding: utf-8 -*-

# Copyright © 2016 Nippon Telegraph and Telephone Corporation

import json
from jubakit.loader.core import LineBasedFileLoader


class KomachiLoader(LineBasedFileLoader):

    def __init__(self, f, *args, include_responses=False, include_votes=False, **kwargs):
        super(KomachiLoader, self).__init__(f, *args, **kwargs)
        self._include_response = include_responses  # レスを含めるか否か
        self._include_votes = include_votes         # 得票数を含めるか否か

    def preprocess(self, ent):
        contents = json.loads(ent['line'])

        # 複数のレスについて、ユーザIDとレスを1つの特徴量にまとめます
        response_user_ids = ""
        response_messages = ""
        if self._include_response:
            responses = contents['responses']
            for response in responses:
                response_user_ids += response['res_userid'] + " "
                response_messages += response['res_message'] + " " 
        contents['response_messages'] = response_messages
        contents['response_user_ids'] = response_user_ids
       
        # 得票数を特徴量にします
        if self._include_votes:
            votes = contents['votes']
            tmp_votes = {}
            for vote in votes:
                tmp_votes[vote['category']] = vote['count']
        
        for i in range(1, 6):
            contents['vote_{}'.format(i)] = tmp_votes[str(i)] if self._include_votes else 0
       
        return contents 

def get_schema_for_classifier():
    from jubakit.classifier import Schema
    return Schema(_get_columns(Schema.IGNORE), Schema.IGNORE)

def get_schema_for_anomaly():
    from jubakit.anomaly import Schema
    return Schema(_get_columns(Schema.ID), Schema.IGNORE)

def get_schema_for_recommender():
    from jubakit.recommender import Schema
    return Schema(_get_columns(Schema.ID), Schema.IGNORE)

def get_schema_for_weight():
    from jubakit.weight import Schema
    return Schema(_get_columns(Schema.IGNORE), Schema.IGNORE)

def _get_columns(object_id_type):
    from jubakit.base import GenericSchema as Schema
    return {
        'topic_id': object_id_type,
        'user_name': Schema.STRING,
        'user_id': Schema.STRING,
        'title': Schema.STRING,
        'message': Schema.STRING,
        'n_response': Schema.NUMBER,
        'group': Schema.STRING,
        'date': Schema.STRING,
        'n_favorite': Schema.NUMBER,
        'face': Schema.STRING,
        'url': Schema.STRING,
        'response_messages': Schema.STRING,
        'response_user_ids': Schema.STRING,
        'vote_1': Schema.NUMBER,
        'vote_2': Schema.NUMBER,
        'vote_3': Schema.NUMBER,
        'vote_4': Schema.NUMBER,
        'vote_5': Schema.NUMBER,
    }
