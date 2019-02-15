#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 21:13:41 2019

@author: felipe
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
sns.set_style("white")
import numpy as np
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

output_path = 'output/'
vereadores_lista = pd.read_csv(output_path+'lista_vereadores.csv')
n_groups = len(vereadores_lista)
df = []
month_spending = []
year = '2019'
month = '01'
nome_valor = {'nome':[], 'valor': []}
for index, vereador in vereadores_lista.iterrows():
    file_name = '{}{}/{}/prestacao_{}_{}_{}.csv'.format(output_path, year, month, vereador['nome_link'], year, month )
    df.append(pd.read_csv(file_name))
    month_spending.append(df[len(df)-1]['valor'].sum())
    nome_valor['nome'].append(vereador['nome'])
    nome_valor['valor'].append(df[len(df)-1]['valor'].sum())
    print(vereador['nome'], vereador['nome_link'], df[len(df)-1]['valor'].sum())

nome_valor = pd.DataFrame.from_dict(nome_valor)
nome_valor = nome_valor.sort_values(by=['valor'])
print(nome_valor)

index = np.arange(n_groups)
index *= 700
bar_width = 300


fig, ax = plt.subplots(figsize=(12,9))
ax.xaxis.grid(linestyle='--') 
ax.set_yticks(index)
ax.set_yticklabels(list(nome_valor['nome']))
ax.set_xlim([0, 9000]) 

#linha de media dos gastos
ax.axvline(np.mean(nome_valor['valor']), color='g', alpha=0.6, label='Média dos gastos '+locale.currency(round(np.mean(nome_valor['valor']),2), grouping = True)) # media dos gastos do mês
x = np.arange(len(vereadores_lista))

#adiciona o valor a frente da barra corespondente
for i, v in enumerate(nome_valor['valor']):
    ax.text(round(v,2) + 30, i*700 - bar_width/3 ,' '+locale.currency(round(v,2), grouping = True), color=(0.1, 0.1, 0.1) )

#adiciona legendas e titulos
plt.xlabel('Gasto em R$')
plt.title('Gastos com verba indenizatória da câmara municipal de Juiz de Fora - MG Janeiro de 2018')
total_gasto = locale.currency( round(sum(nome_valor['valor']), 2), grouping = True )
plt.text(0,14000, 'Gasto com verba indenizatória do mês: '+str(total_gasto))
plt.legend()

plt.barh(index, nome_valor['valor'], bar_width, alpha=0.8)
plt.savefig(output_path+'image/prestacao_'+year+'_'+month+'.svg', bbox_inches="tight")
plt.show()