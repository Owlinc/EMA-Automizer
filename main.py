# 0. Импорты
from samply_handler import *
from anketolog_handler import *
from common_handler import *

# 1. Извлекаем данные об отправке уведомлений за нужный период
period_prompts = get_prompts()

# 2. Извлекаем полученные ответы за нужный период
period_answers = get_all_answers()

# 3. Соединение данных об уведомлениях и данных о полученных ответах
merged_df = match_beeps_date(period_prompts, period_answers)

# 4. Суммируем данные об участии респондентов
summarized_df = summarize_activity(merged_df)

# 5. Форматируем таблички и экспортируем в .xlsx
export_results(summarized_df, merged_df, period_prompts)

# 6. Информируем о выполнении скрипта
print("Работа заверешна. Файлы сформированы!")

