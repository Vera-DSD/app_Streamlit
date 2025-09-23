import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import warnings
warnings.filterwarnings('ignore')

# Name app 
# описание
st.title('Data Analysis')
st.write("Загрузка CSV файла" )
## Загрузка файла 
uploded_file = st.file_uploaded("Загрузка CSV файла", type= 'CSV')
if uploded_file is not None:
    df = pd.read_csv(uploded_file)
    st.write(df.head(10))

else: 
    df.stop()
##проверка наличия пропусков в файле 
missed_values = df.isna().sum()
missed_values = missed_values[missed_values > 0]



if len(missed_values)>0:
    fig, ax = plt.subplots()
    sns.barplot(x = missed_values.index, y= missed_values.values)
    ax.set_title('Пропуски в столбцах')
    st.pyplot(fig)
else:
    st.write('Нет пропусков')
    st.stop
##заполнить пропускки 

##Выгрузить от пропусков файл