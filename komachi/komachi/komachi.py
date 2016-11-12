# -*- coding: utf-8 -*-
import json
import sys
import re
from bs4 import BeautifulSoup

if sys.version_info > (3, 0):
    import urllib.request
else:
    import urllib2
    reload(sys)
    sys.setdefaultencoding('utf-8')
 
BASE_URL = 'http://komachi.yomiuri.co.jp'

GROUPS = {
    '00': '全ジャンル一覧',
    '01': '生活・身近な話題',
    '04': '恋愛・結婚・離婚',
    '05': '妊娠・出産・育児',
    '02': 'キャリア・職場',
    '06': '家族・友人・人間関係',
    '03': '心や体の悩み',
    '07': '美容・ファッション・ダイエット',
    '08': '趣味・教育・教養',
    '09': '旅行・国内外の地域情報',
    '11': '男性から発信するトピ',
    '10': '編集部からのトピ',
    '15': '弁護士に相談するトピ'
}

PAGE_IDS = [str(i) for i in range(1, 10)]


def __html(url):
    if sys.version_info > (3, 0):
        return urllib.request.urlopen(url).read()
    else:
        return urllib2.urlopen(url).read()


def parse_titles_in_day(year, month, day, page_id=1):
    url = '{0}/d/?d={1:02d}{2:02d}{3:02d}&p={4}'.format(BASE_URL, year, month, day, page_id)
    soup = BeautifulSoup(__html(url), 'lxml')
    topics_list = soup.find('table', class_='topicslist').find_all('tr')[1:]
    result = []
    for topics in topics_list:
        ret = dict()
        ret['title'] = topics.find('td', class_='hd').find('a').text.replace('\r\n', '')
        ret['link'] = BASE_URL + topics.find('td', class_='hd').find('a').get('href')
        ret['n_response'] = topics.find('td', class_='res').text
        ret['n_favorite'] = topics.find('td', class_=re.compile('fav*')).text
        ret['date'] = topics.find('td', class_='date').text
        result.append(ret)
    return result

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
    for i, page_id in enumerate(PAGE_IDS):
        ret = parse_title_page(group_id, page_id)
        print('get titles at page {0}/{1}'.format(i+1, len(PAGE_IDS)))
        result.extend(ret)
    return result



def parse_titles():
    result = dict()
    for group_id, group_name in GROUPS.items():
        print('group {0}'.format(group_name))
        ret = parse_titles_in_group(group_id)
        result[group_name] = ret
    return result


def parse_contents(url):
    url = url.split('?g=')[0] + '?o=0&p=0'
    try:
        soup = BeautifulSoup(__html(url), 'lxml')
        for e in soup.findAll('br'):
            e.extract()
        result = dict()
        topic_id = url.split('/')[-1].split('.')[0]
        title = soup.find('td', class_='hd').h1.contents[1]
        print('scraping {0}: {1}'.format(topic_id, title))
        result['url'] = url
        result['topic_id'] = topic_id
        result['title'] = title
        result['group'] = soup.find('div', class_='nav-bread2').find_all('a')[-1].text
        contents = soup.find('td', class_='m')
        result['message'] = contents.find('p').text.replace('\n', '').replace('\r', '')
        result['user_id'] = contents.find('div', class_='uid-t').contents[0].replace('ユーザーID：', '').replace(' ', '')
        result['user_name'] = soup.find('div', class_=re.compile('kao*')).text
        result['face'] = soup.find('div', class_=re.compile('kao...')).get('class')[0]
        result['date'] = soup.find('td', class_='date').contents[1]
        result['n_favorite'] = soup.find('div', class_='additional-info').find('strong', class_=re.compile('fav*')).text
        result['n_response'] = soup.find('div', class_='hm').text.replace('レス数：', '').replace('本', '')
        result['responses'] = []
        reslist = soup.find('table', class_='reslist').find_all('div', class_='inr')
        for response in reslist:
            res = dict()
            res['res_userid'] = response.find('div', class_='uid-r').text.replace('ユーザーID：', '')
            res['res_message'] = response.find('p').text.replace('\n', '').replace('\r', '')
            result['responses'].append(res)
        vote_url = 'http://komachi.yomiuri.co.jp/servlet/GetVoteResult?topic={}&rescategory=1.2.3.4.5'.format(topic_id)
        vote_soup = BeautifulSoup(__html(vote_url), 'lxml')
        votes = json.loads(vote_soup.find('p').text)['result']
        result['votes'] = votes
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None
