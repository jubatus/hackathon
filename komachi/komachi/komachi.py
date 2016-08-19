# -*- coding: utf-8 -*-
import sys
import re
from bs4 import BeautifulSoup

if sys.version_info > (3, 0):
    import urllib.request
else:
    import urllib2

BASE_URL = 'http://komachi.yomiuri.co.jp'

GROUPS = {'00': '全ジャンル一覧',
          '01': '生活・身近な話題',
          '02': '恋愛・結婚・離婚',
          '03': '妊娠・出産・育児',
          '04': 'キャリア・職場',
          '05': '家族・友人・人間関係',
          '06': '心や体の悩み',
          '07': '美容・ファッション・ダイエット',
          '08': '趣味・教育・教養',
          '09': '旅行・国内外の地域情報',
          '10': '男性から発信するトピ',
          '11': '編集部からのトピ',
          '15': '弁護士に相談するトピ'
          }

PAGE_IDS = [str(i) for i in range(1, 10)]


def __html(url):
    if sys.version_info > (3, 0):
        return urllib.request.urlopen(url).read()
    else:
        return urllib2.urlopen(url).read()

def parse_title_page(group_id, page_id):
    url = '{0}?g={1}&o=0&p={2}'.format(BASE_URL, group_id, page_id)
    soup = BeautifulSoup(__html(url), 'lxml')
    topics_list = soup.find('table', class_='topicslist').find_all('tr')[1:]
    result = []
    for topics in topics_list:
        ret = dict()
        ret['group'] = GROUPS[group_id]
        ret['title'] = topics.find('td', class_='hd').find('a').text.replace('\r\n', '')
        ret['link'] = BASE_URL + topics.find('td', class_='hd').find('a').get('href')
        ret['n_response'] = topics.find('td', class_='res').text
        ret['n_favorite'] = topics.find('td', class_=re.compile('fav*')).text
        ret['date'] = topics.find('td', class_='date').text
        rank = topics.find('td', class_='rank').text.replace('位', '')
        if rank == '---':
            rank = '-1'
        ret['rank'] = rank
        result.append(ret)
    return result


def parse_titles_in_group(group_id):
    result = []
    for page_id in PAGE_IDS:
        ret = parse_title_page(group_id, page_id)
        result.extend(ret)
    return result


def parse_titles():
    result = dict()
    for group_id, group_name in GROUPS.items():
        ret = parse_titles_in_group(group_id)
        result[group_name] = ret
    return result


def parse_contents(url):
    try:
        soup = BeautifulSoup(__html(url), 'lxml')
        for e in soup.findAll('br'):
            e.extract()
        result = dict()
        result['url'] = url
        result['group'] = soup.find('div', class_='nav-bread2').find_all('a')[-1].text
        result['title'] = soup.find('td', class_='hd').h1.contents[1]
        contents = soup.find('td', class_='m')
        result['message'] = contents.find('p').text
        result['user_id'] = contents.find('div', class_='uid-t').contents[0].replace('ユーザーID：', "")
        result['user_name'] = soup.find('div', class_=re.compile('kao*')).text
        result['face'] = soup.find('div', class_=re.compile('kao...')).get('class')[0]
        result['date'] = soup.find('td', class_='date').contents[1]
        result['n_favorite'] = soup.find('div', class_='additional-info').find('strong', class_=re.compile('fav*')).text
        result['n_response'] = soup.find('div', class_='hm').text.replace('レス数：', "").replace('本', "")
        result['responses'] = []
        responses = soup.find('table', class_='reslist').find_all('div', class_='inr')
        for response in responses:
            ret = dict()
            ret['res_userid'] = response.find('div', class_='uid-r').text.replace('ユーザーID：', "")
            ret['res_message'] = response.find('p').text
            result['responses'].append(ret)
        return result
    except Exception as e:
        print('ERROR: ', e)
        return None
