#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 15:27:21 2019

@author: felipe
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

output_path = 'output/'
os.makedirs( output_path )


def get_raw_data():
    url = "http://www.camarajf.mg.gov.br/verba.php?leg=2017-2020&ano=2017&mes=01"
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.content

def parse_html(html):
    soup = BeautifulSoup(html)
    vereadores = {'nome': [],  'link': [], 'link_name': []}
    for a in soup.findAll("a", href=True):
        if len(a.text) > 2:
            vereadores['nome'].append(a.text)
            url = a['href']
            vereadores['link'].append(url)
            vereadores['link_name'].append(url[url.find('vereador')+9:url.find('&ano')])
    df = pd.DataFrame.from_dict(vereadores)
    return df

if __name__ == "__main__":
    html = get_raw_data()
    df = parse_html(html)
    df.to_csv(output_path+'lista_vereadores.csv')