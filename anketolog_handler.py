# Импорты
import datetime

import pandas as pd
import requests
from config import *


# Функция для получения данных о заполненном опросе (один опрос)
def get_answers(survey_name, survey_id):

    # 1. Формируем словарь для переддачи ID опросника
    data = {
        "survey_id": survey_id,
        "limit": 1000,
        "date_from": DATETIME_START.date().strftime('%Y-%m-%d'),
        "date_to": DATETIME_END.date().strftime('%Y-%m-%d')
    }

    # 2. Формируем заголовок запроса
    headers = {"X-Anketolog-ApiKey": ANKET_KEY}

    # 3. Формируем запрос для извлечения данных из платформы для извлечения данных
    answers = requests.post(ANKET_API_URL, headers=headers, json=data).json()

    # 4. Проходимся по ответам и записываем нужные
    filtered_df = pd.DataFrame()
    for answer in answers:

        # 5. Определяем подходит ли нам ответ по дате
        finish_date = answer['finish_date']
        if not (pd.to_datetime(finish_date, unit='s') >= DATETIME_START) and (pd.to_datetime(finish_date, unit='s') <= DATETIME_END):
            continue
        # 6. Записываем ID, название опроса и дату ответа в БД
        if not "params" in answer["collector"]:
            continue
        user_id = answer["collector"]["params"][0]["value"]
        finished_date = pd.to_datetime(
            datetime.datetime.fromtimestamp(answer['finish_date']),
            format='%d.%m.%y %H:%M:%S')
        survey = survey_name
        new_df = pd.DataFrame([{"id": user_id, "finished_dt": finished_date, "survey_name": survey}])
        filtered_df = pd.concat([filtered_df, new_df], ignore_index=True)

    # 7. Возвращем DF с подходящими ответам
    return filtered_df


# Функция для получения данных о заполненных опросах (несколько опросов)
def get_all_answers():

    # 1. Создаем заготовку для хранения всех ответов
    all_period_answers = pd.DataFrame()
    for survey in ANKET_SURVEYS_LIST:

        # 2. Извлекаем ответы по опроснику
        survey_df = get_answers(survey[0], survey[1])

        # 3. Добавляем ответы по опроснику в общую базу
        all_period_answers = pd.concat([survey_df, all_period_answers], ignore_index=True)

    # 4. Возвращаем датафрейм со всеми ответами
    all_period_answers.to_excel('answers.xlsx')
    return all_period_answers