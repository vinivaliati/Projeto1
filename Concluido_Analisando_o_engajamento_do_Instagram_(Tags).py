#!/usr/bin/env python
# coding: utf-8

# # Analisando o engajamento do Instagram
# 
# ### O que queremos responder?
# - Qual a tag mais engaja nessas publicações?
#     - Agora queremos olhar apenas tags
# <br><br>
# - Ele também dá alguns direcionamentos:
#     - Podem ignorar a coluna visualizações, queremos entender apenas curtidas, comentários e interações
#     - Tags vazias é que realmente não possuem tag (favor tratar como vazio)

# ### Vamos importar e visualizar a nossa base

# In[56]:


# Importando o pandas
import pandas as pd
import numpy as np
# Usando o mesmo formato dos valores
pd.options.display.float_format = '{:,.2f}'.format


# In[57]:


# Importar a base em excel
base = pd.read_excel("08. Analisando o engajamento no Instagram.xlsx")


# In[58]:


# Apagando a coluna "Visualizações"
base = base.drop("Visualizações",axis=1)


# In[59]:


# Visualizando novamente as 5 primeiras linhas
base.head()


# In[60]:


# Agrupando por tags
base.groupby("Tags")["Curtidas"].mean()


# ### Para conseguir analisar separadamente as tags, podemos dividir linhas com 2 tags em 2 linhas
# - Para isso primeiro vamos usar o split para separar em uma lista com as tags
# - Depois vamos usar o explode para transformar as listas com 2 tags em 2 linhas diferentes

# **O split separa um texto em uma lista baseado em algum separador**

# In[61]:


texto = "O Curso de Ciência de Dados da Hashtag é top!"


# In[62]:


# Se eu não passo nenhum argumento, ele vai separar por espaço
texto.split()


# In[63]:


texto = "O-Curso-de-Ciência-de-Dados-da-Hashtag-é-top!"


# In[64]:


# Se eu não passo nenhum argumento, ele vai separar por espaço
texto.split()


# In[65]:


# Se for outro delimitador, eu preciso informar
texto.split("-")


# In[66]:


# Vamos usar isso para a nossa coluna "Tags"
# Transformando a coluna Tags em uma lista de tags
base.Tags = base.Tags.str.split("/")
base.head()


# **O explode vai separar uma coluna de um DataFrame em 1 linha para cada elemento da lista**

# In[67]:


# Criando o dicionários
dic = {
    "A": [[1,2],3,[4,5,6],[]],
    "B": [1,2,3,4],
}

# Transformando esse dicionário em um DataFrame
base_dic = pd.DataFrame(dic)

base_dic


# In[68]:


# Usando o explode para separar a coluna A
base_dic = base_dic.explode('A')
base_dic


# - Tudo que estiver em lista será separado em 1 linha por elemento da lista
# - Se não tiver na lista, o elemento será mantido
# - Listas vazias vão ter o valor de `NaN`
# <br><br>
# - Para as outras colunas, elas irão repetir os seus valores
# - Inclusive o índice também irá repetir

# In[69]:


# Separando a coluna Tag em 1 linha para cada elemento da lista
base = base.explode('Tags')
base.head()


# ### Fazendo a mesma análise da média por tag

# **Aviso importante: muito cuidado pois as outras colunas serão duplicadas, então não podemos fazer o mesmo cálculo de média que estávamos fazendo**
# <br><br>
# - No arquivo anterior:
# ![08.%20Analisando%20o%20engajamento%20do%20Instagram%20-%20Img3-2.png](attachment:08.%20Analisando%20o%20engajamento%20do%20Instagram%20-%20Img3-2.png)

# In[70]:


# Repetindo o cálculo da média para pessoas
base.groupby('Pessoas')['Curtidas'].mean()


# **Só vamos fazer as análises que envolve tag depois de fazer isso com a base, podemos ver que ao adicionar linhas para analisar a tag, as demais análises ficam incorretas.**

# In[71]:


# Fazendo para Tag
base.groupby('Tags')['Curtidas'].mean()


# In[72]:


# Ordenando por curtidas
base.groupby("Tags")[["Curtidas","Comentários"]].mean().sort_values("Curtidas",ascending=False)


# - **Postagens de promoções são as que mais engajam**
# - **Além de promoções, datas comemorativas e trends também possuem um bom engajamento**

# **E o que está sem tag?**

# In[73]:


# Filtrando valores sem tag
base.loc[base.Tags.isnull()]


# **Da mesma forma que fizemos para Carrossel, poderíamos ter feito para as tags escrevendo "Sem tag" e nesse caso iria aparecer no groupby**

# In[74]:


# Atribuindo o texto sem tag para as colunas onde a tag é NaN
base.loc[base.Tags.isnull(),"Tags"] = "Sem Tag"


# In[75]:


# Mostrando novamente a tabela de curtidas por tag
base.groupby("Tags")[["Curtidas","Comentários"]].mean().sort_values("Curtidas",ascending=False)


# In[76]:


# Podemos voltar como NaN caso a gente queira somente ignorar esses valores conforme orientado
base.loc[base.Tags == 'Sem Tag', 'Tags'] = np.nan


# In[77]:


# E voltamos com as colunas com valores nulos
base.loc[base.Tags.isnull()]


# In[78]:


# E essas linhas novamente param de ser consideradas na agregação
base.groupby("Tags")[["Curtidas","Comentários"]].mean().sort_values("Curtidas",ascending=False)


# **Agora analisando as tags com pessoas e campanhas:**

# In[83]:


# Fazendo para Pessoas e Tag
base.groupby(["Pessoas","Tags"])[["Curtidas","Comentários"]].mean()


# In[85]:


# Também podemos ordenar por curtidas
base.groupby(["Pessoas","Tags"])[["Curtidas","Comentários"]].mean().sort_values("Curtidas", ascending=False)


# In[86]:


# Fazendo para Campanhas e Tag
base.groupby(["Campanhas","Tags"])[["Curtidas","Comentários"]].mean().sort_values("Curtidas", ascending=False)


# ## Conclusões
# - **Ter o rosto de outras pessoas é fundamental para um bom engajamento na publicação**
#     - Em todas as tags, quando havia o rosto, o resultado foi muito melhor
# - **Criar campanhas ajuda muito na divulgação da marca**
# - **Promoções tiveram um desempenho absurdamente maior que qualquer outra tag**
#     - Porém é uma tag que pode ter custo para a loja, o que deve ser analisado
# - **Usar conteúdos que estão em trend também ajudam na divulgação da marca, mesmo a trend sendo de outros nichos**
# - **A melhor maneira de mostrar produtos é através de outras pessoas utilizando-os, e se possível em campanhas de datas especiais**
# - **Para novos produtos a inclusão de pessoas é mais crítica ainda, sendo quase o dobro quando há um rosto junto ao produto**
# - **Não podemos afirmar que a tag `Loja` é ruim até testarmos essa tag incluindo pessoas ou em uma campanha. Vale o teste para verificar**
# - **Continuaremos a monitorar as postagens para encontrar novos padrões dado que ainda temos poucas informações da base**
