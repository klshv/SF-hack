import streamlit as st
import pandas as pd
import codecs
import json
from datetime import date


st.set_page_config(page_title="Поиск авиабилетов", page_icon=":airplane:", layout="wide")

# Введите логин и пароль
username = st.sidebar.text_input("Логин")
password = st.sidebar.text_input("Пароль", type="password")

# Аутентификация пользователя
if st.sidebar.checkbox("Войти"):
    if username == "admin" and password == "12345":
        st.success("Успешная аутентификация")
    else:
        st.error("Неправильный логин или пароль")

def load_css(file_name:str)->None:
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("styles.css")

# Чтение содержимого HTML-файла
with open("header.html") as f:
    header_html = f.read()

# Отображение заголовка с помощью st.markdown()
st.markdown(header_html, unsafe_allow_html=True)


# Форма поиска билетов
with st.form(key='flight_search_form'):
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    departure = col1.text_input("Город отправления:")
    arrival = col2.text_input("Город прибытия:")
    departure_date = col3.date_input("Дата вылета:", date.today())
    arrival_date = col4.date_input("Дата прилета:", date.today())

    col5, col6 = st.columns([1, 1])
    class_type = col5.selectbox("Класс:", ("Эконом", "Бизнес", "Первый"))
    passengers = col6.number_input("Количество пассажиров:", min_value=1, max_value=10, value=1)

    search_button = st.form_submit_button(label="Найти билеты 🔍")

# Если форма была отправлена, отобразить результаты поиска
if search_button:

    sort_by = st.selectbox('Сортировка по', ['Цена по возрастанию', 'Цена по убыванию', 'Длительность по возрастанию', 'Длительность по убыванию'])

    # Создание словаря с данными пользователя
    user_data = {
        'departure': departure,
        'arrival': arrival,
        'departure_date': str(departure_date),
        'arrival_date': str(arrival_date),
        'class_type': class_type,
        'passengers': passengers
    }

    # Сериализация словаря в формат JSON
    json_data = json.dumps(user_data, ensure_ascii=False)

    # Запись JSON-данных в файл в читаемом формате
    with codecs.open('user_data.json', 'w', encoding='utf8') as f:
        f.write(json_data)


    # Загрузка данных
    data = pd.read_csv('train_data.csv')

    # Удаление первого столбца
    data = data.drop(data.columns[0], axis=1)

    # Переименование столбцов
    data = data.rename(columns={
        'airline': 'Авиакомпания',
        'flight': 'Рейс',
        'source_city': 'Город отправления',
        'departure_time': 'Время отправления',
        'stops': 'Пересадки',
        'arrival_time': 'Время прибытия',
        'destination_city': 'Город прибытия',
        'class': 'Класс',
        'duration': 'Длительность, ч',
        'days_left': 'Дней до вылета',
        'price': 'Цена, руб'
    })

     # Функция для преобразования значения времени дня в формат времени
    def convert_time(time):
        if time == 'Night':
            return '01:10'
        elif time == 'Evening':
            return '20:15'
        elif time == 'Morning':
            return '07:35'
        elif time == 'Afternoon':
            return '13:05'
        else:
            return time

    # Преобразование значений времени прибытия
    data['Время прибытия'] = data['Время прибытия'].apply(convert_time)

    if sort_by == 'Цена по возрастанию':
        data_sorted = data.sort_values(by=['Цена, руб'], ascending=True)
    elif sort_by == 'Цена по убыванию':
        data_sorted = data.sort_values(by=['Цена, руб'], ascending=False)
    elif sort_by == 'Длительность по возрастанию':
        data_sorted = data.sort_values(by=['Длительность, ч'], ascending=True)
    elif sort_by == 'Длительность по убыванию':
        data_sorted = data.sort_values(by=['Длительность, ч'], ascending=False)
    else:
        data_sorted = data

    # Генерация HTML-кода таблицы с отсортированными данными
    html_table_sorted = data_sorted.to_html(index=False, classes=["styled-table"])

    # Отображение таблицы с помощью st.write
    st.write(html_table_sorted, unsafe_allow_html=True)



    