#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 16:22:17 2019

@author: felipe
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

output_path = 'output/'

def mkdir_output_folders():
    
    years = ['2017','2018','2019']
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for year in years:
        for month in months:
            if os.path.exists(output_path+year+'/'+month) != True:
                os.makedirs( output_path+year+'/'+month )
            

def get_raw_data(url):    
    r = requests.get(url)
    r.encoding = 'utf-8'
    return r.content

'''
    leg - se refere ao exercicio do mandato ano de inicio (4 digitos) - ano final (4 digitos)
          exemplo: 2017-2020
    vereador - extraido de lista_vereadores.csv
    ano - 4 digitos
    mes - 2 digitos
'''
def build_url(link_name, ano, mes):
    url_base = 'http://www.camarajf.mg.gov.br/verba.php?leg=2017-2020&verba=1&vereador={}&ano={}&mes={}'.format(link_name, str(ano), str(mes))
    return url_base

def parse_html(html):
    soup = BeautifulSoup(html)
    table = soup.findAll("table", id="AutoNumber2")[0]
    contas = {'Documento': [], 'Data Emissão': [], 'Emitente': [], 'CPF/CNPJ': [], 'Valor': []}
    cont = 0
    for tr in table.findAll('tr')[4:]:
        if cont % 2 != 0:
            row = [td.text.strip() for td in tr.findAll('td')]
            if len(row) == 5:
                for i in range(len(contas)):
                    contas[list(contas.keys())[i]].append(row[i])
        cont +=1
    df = pd.DataFrame.from_dict(contas)
    return df

if __name__ == "__main__":

    df = pd.read_csv('output/lista_vereadores.csv')
    mkdir_output_folders() # cria os diretorios 
    years = ['2017','2018','2019']
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    
    for vereador in df['link_name']:
        for year in years:
            for month in months: 
                url = build_url(vereador, year, month)
                html = get_raw_data(url)
                df = parse_html(html)
                df.to_csv(output_path+'{}/{}/prestacao_{}_{}_{}.csv'.format(year, month, vereador, year, month))