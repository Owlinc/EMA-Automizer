import pandas as pd
from selenium import webdriver

# Условия для фильтрации
DATETIME_START = pd.to_datetime('2023-11-20 00:00:00')
DATETIME_END = pd.to_datetime('2023-11-20 23:59:00')

# Данные для платформы, рассылающей промпты
PROMPTS_URL = "https://samply.uni-konstanz.de/"
PROMPTS_USER_EMAIL = "************"
PROMPTS_USER_PASSWORD = "************"

# Данные для платформы, принимающей ответы
ANKET_KEY = "************"
ANKET_SURVEYS_LIST = [
    ['Забота о себе (Утро)', 774330],
    ['Забота о себе (День)', 774475],
]
ANKET_API_URL = "https://apiv2.anketolog.ru/survey/answer/list"

# Драйвер для работы с сайтами
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
driver = webdriver.Chrome()
driver.options = options
