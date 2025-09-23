importimport streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf 
from datetime import datetime, timedelta
import seaborn as sns

# Настройка страницы
st.set_page_config(
    page_title="Финансовый анализ - Apple и Tips",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Заголовок приложения
st.title('📊 Финансовый аналитический центр')
st.markdown('---')

# Боковая панель
st.sidebar.title("🎛️ Панель управления")

# Кнопка загрузки файла - ПРАВИЛЬНОЕ РАСПОЛОЖЕНИЕ
st.sidebar.header("📁 Загрузка файлов")
uploaded_file = st.sidebar.file_uploader("Загрузите CSV файл", type=['csv'], 
                                       help="Для использования в разделе Tips Analysis")

# Навигация
page = st.sidebar.radio("Выберите раздел:", 
                       ["🏠 Главная страница", 
                        "📈 Анализ акций Apple", 
                        "🍽️ Анализ данных Tips"])

# Главная страница
if page == "🏠 Главная страница":
    st.header("🏠 Добро пожаловать в финансовый аналитический центр!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📈 О разделе Apple Stock Analysis
        
        **Возможности анализа акций Apple:**
        - 📊 Загрузка реальных данных в реальном времени
        - 📈 Графики цен закрытия и объемов торгов
        - 💹 Технические индикаторы и метрики
        - 📋 Исторические данные за разные периоды
        - 💾 Скачивание данных в CSV формате
        
        **Доступные периоды:** 1 месяц, 3 месяца, 1 год
        """)
    
    with col2:
        st.markdown("""
        ### 🍽️ О разделе Tips Analysis
        
        **Возможности анализа данных Tips:**
        - 📁 Загрузка собственных CSV файлов
        - 📊 Визуализация взаимосвязей данных
        - 📈 Статистический анализ показателей
        - 🎯 Сравнение по различным категориям
        - 💾 Экспорт результатов анализа
        
        **Используются демо-данные** или ваши собственные файлы
        """)
    
    st.markdown("---")
    st.success("👈 Выберите раздел для анализа в меню слева!")

# Раздел Apple - ИСПРАВЛЕННАЯ ВЕРСИЯ
elif page == "📈 Анализ акций Apple":
    st.header("📈 Анализ акций Apple (AAPL)")
    
    # Настройки
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Настройки анализа")
        period = st.selectbox(
            "Выберите период для анализа:",
            ["1mo", "3mo", "6mo", "1y", "2y"],
            index=3,
            key="apple_period"
        )
    
    with col2:
        st.subheader("Дополнительно")
        show_volume = st.checkbox("Показать объемы торгов", value=True, key="apple_volume")
    
    # УПРОЩЕННАЯ загрузка данных Apple
    try:
        with st.spinner('🔄 Загружаем данные Apple...'):
            # Пробуем простую загрузку
            data = yf.download("AAPL", period=period, progress=False)
            
            if data.empty or len(data) == 0:
                st.warning("⚠️ Не удалось загрузить реальные данные. Используем демо-данные.")
                # Создаем демо-данные
                dates = pd.date_range(end=datetime.now(), periods=60, freq='D')
                np.random.seed(42)
                
                base_price = 170
                prices = []
                current = base_price
                
                for i in range(len(dates)):
                    change = np.random.normal(0, 1.5)
                    current = max(100, current + change)
                    prices.append(current)
                
                data = pd.DataFrame({
                    'Open': [p * 0.995 for p in prices],
                    'High': [p * 1.015 for p in prices],
                    'Low': [p * 0.985 for p in prices],
                    'Close': prices,
                    'Volume': np.random.randint(2000000, 8000000, len(dates))
                }, index=dates)
            
            # Очистка данных
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                if col in data.columns:
                    data[col] = pd.to_numeric(data[col], errors='coerce')
            
            data = data.dropna()
            
            if len(data) > 0:
                st.success(f"✅ Данные загружены! Записей: {len(data)}")
                
                # Безопасное получение цен
                close_prices = data['Close'].values
                current_price = float(close_prices[-1])
                
                if len(close_prices) > 1:
                    prev_price = float(close_prices[-2])
                    change = current_price - prev_price
                    change_pct = (change / prev_price) * 100
                else:
                    prev_price = current_price
                    change = 0
                    change_pct = 0
                
                # Основные метрики
                st.subheader("📊 Ключевые показатели")
                col1, col2, col3, col4 = st.columns(4)
                
                col1.metric("Текущая цена", f"${current_price:.2f}", f"{change:+.2f}")
                col2.metric("Изменение %", f"{change_pct:+.2f}%")
                col3.metric("Максимум", f"${data['High'].max():.2f}")
                col4.metric("Минимум", f"${data['Low'].min():.2f}")
                
                # Графики
                tab1, tab2 = st.tabs(["📈 Графики", "📋 Данные"])
                
                with tab1:
                    # Основной график цен
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.plot(data.index, data['Close'], linewidth=2, color='blue')
                    ax.set_title(f"Акции Apple (AAPL) - {period}")
                    ax.set_ylabel("Цена ($)")
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
                    plt.close(fig)
                    
                    # График объемов
                    if show_volume:
                        fig2, ax2 = plt.subplots(figsize=(12, 4))
                        ax2.bar(data.index, data['Volume'], alpha=0.7, color='orange')
                        ax2.set_ylabel("Объем")
                        ax2.grid(True, alpha=0.3)
                        st.pyplot(fig2)
                        plt.close(fig2)
                
                with tab2:
                    # Данные
                    st.subheader("Исторические данные")
                    display_data = data.round(2)
                    st.dataframe(display_data.tail(10))
                    
                    # Статистика
                    st.subheader("Статистика")
                    stats = data.describe().round(2)
                    st.dataframe(stats)
                    
                    # Скачивание
                    st.subheader("💾 Скачивание данных")
                    csv_data = data.to_csv().encode('utf-8')
                    st.download_button(
                        label="📥 Скачать данные Apple",
                        data=csv_data,
                        file_name=f"apple_data_{period}.csv",
                        mime="text/csv"
                    )
            else:
                st.error("❌ Нет данных для отображения")
                
    except Exception as e:
        st.error(f"❌ Ошибка: {str(e)}")
        st.info("Попробуйте перезагрузить страницу или выбрать другой период")

# Раздел Tips - УПРОЩЕННАЯ ВЕРСИЯ
elif page == "🍽️ Анализ данных Tips":
    st.header("🍽️ Анализ данных Tips")
    
    # Создаем данные Tips
    def create_tips_data():
        np.random.seed(42)
        n = 100
        
        data = {
            'total_bill': np.round(np.random.uniform(10, 50, n), 2),
            'tip': np.round(np.random.uniform(1, 10, n), 2),
            'size': np.random.randint(1, 6, n),
            'day': np.random.choice(['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'], n),
            'time': np.random.choice(['Обед', 'Ужин'], n)
        }
        
        df = pd.DataFrame(data)
        df['tip'] = df['tip'].clip(lower=1.0)
        return df
    
    # Используем загруженный файл или создаем данные
    if uploaded_file is not None:
        try:
            tips_data = pd.read_csv(uploaded_file)
            st.success(f"✅ Загружен файл: {uploaded_file.name}")
        except Exception as e:
            st.error(f"❌ Ошибка загрузки файла: {e}")
            tips_data = create_tips_data()
            st.info("ℹ️ Используются демо-данные")
    else:
        tips_data = create_tips_data()
        st.info("ℹ️ Используются демо-данные Tips")
    
    st.success(f"✅ Данные загружены! Записей: {len(tips_data)}")
    
    # Основные метрики
    col1, col2, col3 = st.columns(3)
    col1.metric("Всего записей", len(tips_data))
    col2.metric("Средний чек", f"${tips_data['total_bill'].mean():.2f}")
    col3.metric("Средние чаевые", f"${tips_data['tip'].mean():.2f}")
    
    # Графики
    tab1, tab2 = st.tabs(["📈 Графики", "📋 Данные"])
    
    with tab1:
        # Scatter plot
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.scatter(tips_data['total_bill'], tips_data['tip'], alpha=0.6)
        ax1.set_xlabel('Сумма счета ($)')
        ax1.set_ylabel('Чаевые ($)')
        ax1.set_title('Связь суммы счета и чаевых')
        ax1.grid(True, alpha=0.3)
        st.pyplot(fig1)
        plt.close(fig1)
        
        # Гистограмма
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.hist(tips_data['total_bill'], bins=15, alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Сумма счета ($)')
        ax2.set_ylabel('Количество')
        ax2.set_title('Распределение суммы счета')
        st.pyplot(fig2)
        plt.close(fig2)
    
    with tab2:
        # Данные
        st.dataframe(tips_data.head(10))
        
        # Статистика
        st.subheader("Статистика")
        st.dataframe(tips_data.describe().round(2))
        
        # Скачивание данных Tips
        csv_data = tips_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Скачать данные Tips",
            data=csv_data,
            file_name="tips_data.csv",
            mime="text/csv"
        )

# Футер приложения
st.markdown("---")
st.markdown("### 📱 О приложении")
st.markdown("""
**Финансовый аналитический центр** - образовательное приложение для анализа данных
""")

# Информация в боковой панели
st.sidebar.markdown("---")
st.sidebar.info("""
**Справка:**
- Данные Apple обновляются в реальном времени
- Tips данные можно заменить своими CSV файлами
""")

if st.sidebar.button("🔄 Перезагрузить приложение"):
    st.rerun()