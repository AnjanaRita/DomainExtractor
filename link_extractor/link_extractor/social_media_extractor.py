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
PUNCT = '!"#$%\'&()*+-/:,;<=>?@[\\]^_`{|}~'
INVALID_LIST = ['youtube','yelp', 'google', 'yellowpage', 'wikipedia','facebook','maprequest','bloomberg']
SM = ['facebook','linkedin','twitter','youtube','github', 'google plus', 'pinterest', 'instagram',
 'snapchat', 'flipboard', 'flickr', 'weibo', 'periscope', 'telegram', 'soundcloud', 'feedburner', 'vimeo',
 'slideshare', 'vkontakte', 'xing']

class SocialMedia:
    def __init__(self,link, social_media = None):
        self.link = self.domain_extracted(link)
        self.social_media = social_media
        if self.social_media:
            self.SM = social_media
        else:
            self.SM = SM
        self.DEFAULT_DICT = {j:[] for j in self.SM}
    
    @property
    def social_links(self):
        link = self.link
        if pd.isnull(link):
            return {}
        try:
            all_links = self.get_alllinks(link, self.req)
            contact_us_link = self.get_contact_us_link(all_links, link)
            sm_link = self.get_social_media_links(contact_us_link, self.SM, self.DEFAULT_DICT.copy())
            return sm_link
        except Exception as ex:
            try:
                sm_link = self.get_social_media_links(link, self.SM, self.DEFAULT_DICT.copy())
                return sm_link
            except Exception as ex:
                return self.DEFAULT_DICT.copy()
            
    @staticmethod
    def domain_extracted(link):
        try:
            temp = link.split("://")
            domain=  temp[0]+'://' + temp[1].split('/')[0]
            return domain
        except Exception:
            return np.nan
    

    def get_alllinks(self, link):
        page = requests.get(link,verify=False, timeout=30)
        soup = BeautifulSoup(page.text, 'html.parser')
        links = []
        for link in soup.find_all('a', href=True):
            links.append(link['href'])
        return links

    def get_contact_us_link(self,all_links, link):
        valid_url = ''
        return_link = link
        has_contact_link = False
        for _link in all_links:
            if 'contact' in _link:
                valid_url = _link
                has_contact_link = True
                break
        if has_contact_link:
            if link in valid_url:
                return_link = valid_url
            else:
                return_link = link+valid_url
        return return_link
    
    def get_social_media_links(self,link, DEFAULT_SM, default_dict):
        res = requests.get(link,verify=False, timeout=30)
        tree = parse_html_bytes(res.content, res.headers.get('content-type'))
        sm_link =  list(find_links_tree(tree))
        for i in sm_link:
            for sm in DEFAULT_SM:
                if sm in i:
                    default_dict[sm] += [i]
        return default_dict