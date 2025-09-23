import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf 
import numpy as np

# Настройка страницы
st.set_page_config(
    page_title="Анализ данных",
    page_icon="📊",
    layout="wide"
)

# Заголовок
st.title('📊 Анализ данных Apple & Tips')
st.markdown('---')

# Боковая панель
st.sidebar.title("🎛️ Панель управления")
page = st.sidebar.radio("Выберите раздел:", 
                       ["🏠 Главная страница", 
                        "📈 Анализ акций Apple", 
                        "🍽️ Анализ данных Tips"])

# Кнопка загрузки файла 
st.sidebar.header("📁 Загрузка файлов")
uploaded_file = st.sidebar.file_uploader("Загрузите CSV файл", type=['csv'], 
                                       help="Для использования в разделе Tips Analysis")

# Главная страница
if page == "🏠 Главная страница":
    st.header("Добро пожаловать!")
    st.write("Выберите раздел для анализа в меню слева")

# Раздел Apple
elif page == "📈 Анализ акций Apple":
    st.header("📈 Акции Apple (AAPL)")
    
    # Простые настройки
    period = st.selectbox("Период:", ["1mo", "3mo", "6mo", "1y"], index=2)
    
    try:
        # Загрузка данных
        data = yf.download("AAPL", period=period)
        
        if len(data) > 0:
            # Простые метрики
            current_price = float(data['Close'].iloc[-1])
            prev_price = float(data['Close'].iloc[-2]) if len(data) > 1 else current_price
            
            st.metric("Текущая цена", f"${current_price:.2f}", 
                     f"${current_price - prev_price:.2f}")
            
            # Простой график
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(data.index, data['Close'].astype(float), linewidth=2)
            ax.set_title("Цена акций Apple")
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            plt.close(fig)
            
            # Таблица данных
            st.write("Последние 5 записей:")
            display_data = data.tail().copy()
            # Упрощенное отображение данных
            st.dataframe(display_data.round(2))
            
            # Скачивание данных Apple
            csv_data = data.to_csv().encode('utf-8')
            st.download_button(
                label="📥 Скачать данные Apple",
                data=csv_data,
                file_name=f"apple_data_{period}.csv",
                mime="text/csv"
            )
            
        else:
            st.write("Нет данных для отображения")
            
    except Exception as e:
        st.write("Ошибка загрузки данных")
        st.write(str(e))

# Раздел Tips
elif page == "🍽️ Анализ данных Tips":
    st.header("📋 Анализ данных Tips")
    
    # Создаем простые данные Tips
    def create_tips_data():
        np.random.seed(42)
        n = 100
        
        data = {
            'total_bill': np.round(np.random.uniform(10, 50, n), 2),
            'tip': np.round(np.random.uniform(1, 10, n), 2),
            'size': np.random.randint(1, 6, n),
            'day': np.random.choice(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], n),
            'time': np.random.choice(['Lunch', 'Dinner'], n)
        }
        
        df = pd.DataFrame(data)
        df['tip'] = df['tip'].clip(lower=1.0)
        return df
    
    # Используем загруженный файл или создаем данные
    if uploaded_file is not None:
        try:
            tips_data = pd.read_csv(uploaded_file)
            st.success(f"Загружен файл: {uploaded_file.name}")
        except Exception as e:
            st.error(f"Ошибка загрузки: {e}")
            tips_data = create_tips_data()
            st.info("Используются демо-данные")
    else:
        tips_data = create_tips_data()
        st.info("Используются демо-данные Tips")
    
    st.write(f"Всего записей: {len(tips_data)}")
    
    # Основные статистики
    col1, col2, col3 = st.columns(3)
    col1.metric("Средний чек", f"${tips_data['total_bill'].mean():.2f}")
    col2.metric("Средние чаевые", f"${tips_data['tip'].mean():.2f}")
    col3.metric("Размер группы", f"{tips_data['size'].mean():.1f}")
    
    # Простые графики
    tab1, tab2 = st.tabs(["Графики", "Данные"])
    
    with tab1:
        # График 1
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        ax1.scatter(tips_data['total_bill'], tips_data['tip'], alpha=0.6)
        ax1.set_xlabel("Сумма счета ($)")
        ax1.set_ylabel("Чаевые ($)")
        ax1.set_title("Связь суммы счета и чаевых")
        ax1.grid(True, alpha=0.3)
        st.pyplot(fig1)
        plt.close(fig1)
        
        # График 2
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.hist(tips_data['total_bill'], bins=15, alpha=0.7, edgecolor='black')
        ax2.set_xlabel("Сумма счета ($)")
        ax2.set_ylabel("Количество")
        ax2.set_title("Распределение суммы счета")
        st.pyplot(fig2)
        plt.close(fig2)
    
    with tab2:
        st.write("Первые 10 записей:")
        st.dataframe(tips_data.head(10))
        
        st.write("Основные статистики:")
        st.dataframe(tips_data.describe().round(2))
        
        # Скачивание данных Tips - ПРАВИЛЬНОЕ РАСПОЛОЖЕНИЕ
        csv_data = tips_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Скачать данные Tips",
            data=csv_data,
            file_name="tips_data.csv",
            mime="text/csv"
        )

st.markdown('---')
st.write("© Приложение для анализа данных")
