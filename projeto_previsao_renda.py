import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

sns.set(context='talk', style='ticks')

def plotbarDf (data,x):
     crossData = pd.crosstab(data['data_ref'].dt.to_period('M'),data[x])
     crossData = crossData.div(crossData.sum(axis=1),axis=0)
     crossData.plot.bar(stacked =True,rot=70,figsize=(10, 3),title=x);
     plt.legend(
     title=x,
     loc="upper left", 
     bbox_to_anchor=(1, 1) 
     )
     st.pyplot(plt)

st.set_page_config(
     page_title="Análise de crédito",
     page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCnozxswARq7e6VGmVoGm4Y-6ZUTIJXG15Ig&s",
     layout = 'wide'
)

st.write('# Análise exploratória da previsão de renda')





st.sidebar.write('# Enviar Arquivo')
arquivo = st.sidebar.file_uploader("Carregar base de clientes para análise", type="csv")

if arquivo is not None:
     df_renda = pd.read_csv(arquivo).drop(columns=['Unnamed: 0', 'id_cliente'])

     df_renda.data_ref = pd.to_datetime(df_renda.data_ref)
     min_data = df_renda.data_ref.min()
     max_data = df_renda.data_ref.max()

     data_inicial = pd.to_datetime(st.sidebar.date_input('Data Inicial',
               value = min_data,
               min_value = min_data,
               max_value = max_data))

     data_final = pd.to_datetime(st.sidebar.date_input('Data Inicial',
               value = max_data,
               min_value = min_data,
               max_value = max_data))
     
     df_renda_filtrado = df_renda[(df_renda.data_ref <= data_final)&(df_renda.data_ref >= data_inicial)]
     #st.write(df_renda_filtrado)

     fig, ax = plt.subplots(4,2,figsize=(20,40))
     st.subheader('Análise por Renda')
     sns.barplot(x='posse_de_imovel',y='renda',data=df_renda_filtrado,ax=ax[0,0],palette='RdBu')
     ax[0, 0].set_title('Imóvel X Renda', fontsize=20)

     sns.barplot(x='posse_de_veiculo',y='renda',data=df_renda_filtrado,ax=ax[0,1],palette='RdBu')
     ax[0, 1].set_title('Veículo X Renda', fontsize=20)

     sns.barplot(x='qtd_filhos',y='renda',data=df_renda_filtrado,ax=ax[1,0],palette='RdBu')
     ax[1, 0].set_title('Filhos X Renda', fontsize=20)

     sns.barplot(x='tipo_renda',y='renda',data=df_renda_filtrado,ax=ax[1,1],palette='RdBu')
     ax[1, 1].set_title('Tipo de Renda X Renda', fontsize=20)
     ax[1,1].tick_params(axis='x', rotation=45)

     sns.barplot(x='educacao',y='renda',data=df_renda_filtrado,ax=ax[2,0],palette='RdBu')
     ax[2, 0].set_title('Educação X Renda', fontsize=20)
     ax[2,0].tick_params(axis='x', rotation=45)

     sns.barplot(x='estado_civil',y='renda',data=df_renda_filtrado,ax=ax[2,1],palette='RdBu')
     ax[2, 1].set_title('Estado Civil X Renda', fontsize=20)

     sns.barplot(x='qt_pessoas_residencia',y='renda', data=df_renda_filtrado, ax=ax[3,0], palette='RdBu')
     ax[3, 0].set_title('Pessoas Residência', fontsize=20)

     sns.barplot(x='tipo_residencia',y='renda',data=df_renda_filtrado,ax=ax[3,1],palette='RdBu')
     ax[3, 1].set_title('Tipo Residência X Renda', fontsize=20)
     ax[3,1].tick_params(axis='x', rotation=45)

     fig.tight_layout(pad=1.0)
     st.pyplot(plt)


     st.subheader('Média de Renda por Idade')
     plt.figure(figsize=(10, 6))
     sns.lineplot(x='idade', y='renda', data=df_renda_filtrado, estimator=lambda x: sum(x) / len(x), palette='RdBu')
     plt.xticks(rotation=45)
  
     st.pyplot(plt)

     st.write('# Avaliação das variáveis Quantitativas')

     df_renda_qt = df_renda_filtrado.select_dtypes(include=['int','float'])
     plt.figure(figsize=(20,10))
     sns.pairplot(df_renda_qt)
     st.pyplot(plt)


     st.write('# Avaliação das variáveis Qualitativas')

     df_renda_qualt = df_renda_filtrado.select_dtypes(exclude=['int','float'])

     df_renda_qualt.drop(columns=['data_ref']).columns.map(lambda x:plotbarDf(df_renda_qualt,x));



