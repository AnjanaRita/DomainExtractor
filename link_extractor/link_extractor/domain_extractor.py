import os
import re
import json
import time
import random
import urllib3
import requests
import pandas as pd
import numpy as np
import urllib.request
from lxml import html
from tqdm import tqdm
import multiprocessing
import jellyfish as jf

from cleanco import cleanco
from ast import literal_eval
from bs4 import BeautifulSoup
from torrequest import TorRequest
from torrequest import TorRequest
from html_to_etree import parse_html_bytes
from extract_social_media import find_links_tree
from .resource import user_agents

LINK_1 = 'h2/a/@href'
TITLE = 'h2/a/text()'
RESULT = '//li[@class="b_algo"]'
URL = 'https://www.bing.com/search?q='
TEXT = 'div[@class="b_caption"]/p//text()'
CMP_NAME = './/h2[@class=" b_entityTitle"]//text()'
HREF_URL = '//div[@class="b_subModule"]//*[@class="b_hList"]//a/@href'
ADDRESS = './/*[@class="bm_details_overlay"]//a/text()'

PUNCT = '!"#$%\'&()*+-/:,;<=>?@[\\]^_`{|}~'
INVALID_LIST = ['youtube','yelp', 'google', 'yellowpage', 'wikipedia','facebook','maprequest','bloomberg']
SM = ['facebook','linkedin','twitter','youtube','github', 'google plus', 'pinterest', 'instagram',
 'snapchat', 'flipboard', 'flickr', 'weibo', 'periscope', 'telegram', 'soundcloud', 'feedburner', 'vimeo',
 'slideshare', 'vkontakte', 'xing']

class DomainExtractor:
    def __init__(self, name ,invalid_link= None, enable_tor=True,password= None):
        self.name = name
        self.enable_tor = enable_tor
        self.invalid_link = invalid_link
        self.password = password
        if self.enable_tor and self.password:
            self.req=TorRequest(password=self.password)
        else:
            self.req = requests
        if self.invalid_link:
            self.INVALID = INVALID_LIST + invalid_link
        else:
            self.INVALID = INVALID_LIST
        
    @property
    def domain(self):
        data = self._get_block(self.name,self.req)
        if data['LINK'] == []:
            data = self._get_data(self.name, self.req)
        link = self.get_valid_link(data['LINK'], self.INVALID+SM)
        return {'DOMAIN':link, 'ADDRESS': data['ADDRESS'],'COMPANY_NAME': data['COMPANY_NAME']}

    def _get_block(self, name, req):
        try:
            data = {}
            url = self._get_bing_query(name)
            res = req.get(url, headers={'User-Agent':random.choice(user_agents)})
            parser = html.fromstring(res.text)
            links = [i for i in parser.xpath(HREF_URL) if i.startswith('http')]
            links = [lk for lk in links if self.is_valid(lk,INVALID_LIST+SM)]
            data['COMPANY_NAME'] = ' '.join(parser.xpath(CMP_NAME))
            data['ADDRESS'] = ' '.join(parser.xpath(ADDRESS))
            data['SEARCH_URL'] = url
            data['LINK'] = links
            return data
        except:
            return {'COMPANY_NAME':[],'ADDRESS':[],'LINK':[]}
        

    def _get_data(self,name, req):
        try:
            url = self._get_bing_query(name)
            res = req.get(url, headers={'User-Agent':random.choice(user_agents)})
            parser = html.fromstring(res.text)
            total_block = parser.xpath(RESULT)
            link_1 = total_block[0].xpath(LINK_1)
            title_1 = total_block[0].xpath(TITLE)
            link_2 = total_block[1].xpath(LINK_1)
            title_2 = total_block[1].xpath(TITLE)
            tup = (name, title_1, link_1, title_2, link_2)
            return_data = {'LINK':sum([link_1,link_2],[]),'TITLE':[title_1, title_2],'COMPANY_NAME':None,
            'ADDRESS':None}
        except:
            return_data = {'LINK':[],'TITLE':[],'COMPANY_NAME':None,'ADDRESS':None}
        return return_data
    

    def _get_bing_query(self,name):
        name = self._clean_text(name, False)
        url = URL+name
        return url
    
    
    def _clean_text(self,name,lower=True):
        try:
            if name:
                name = name.strip().lower()
                name = name.translate(str.maketrans(' ', ' ', PUNCT))
                name = re.sub('\s\s+',' ',name)
                name = cleanco(name).clean_name()
                #name = name + ' website'
                name = name.replace(' ','+')
                return name
            return name
        except Exception as ex:
            return ''
        
    def is_valid(self,link,INVALID_LIST):
        count = 0
        for i in INVALID_LIST:
            if i in link:
                count+=1
        if count:
            return False
        else:
            return True

    def get_valid_link(self,links,INVALID_LIST):
        return_link = np.nan
        for link in links:
            if self.is_valid(link,INVALID_LIST):
                return_link = link
                break
        return return_link