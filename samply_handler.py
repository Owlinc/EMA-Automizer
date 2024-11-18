# Импорты
from config import *
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import re


# Функция для получения данных об отправленных уведомлениях
def get_prompts():

    try:
        # 1. Заходим на сайт платформы, отправляющей уведомления
        driver.get(PROMPTS_URL)
        driver.maximize_window()

        # 2. Переходим к странице входа
        time.sleep(0.1)
        driver.find_element(By.XPATH, '/html/body/header/nav/div[2]/li[1]/a').click()

        # 3. Находим поля авторизации
        email_input = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/form/input[1]')
        password_input = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/form/input[2]')

        # 4. Очищаем поля авторизации
        email_input.clear()
        password_input.clear()

        # 5. Вводим данные пользователя
        email_input.send_keys(PROMPTS_USER_EMAIL)
        password_input.send_keys(PROMPTS_USER_PASSWORD)

        # 6. Авторизуемся
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/form/input[3]').click()

        # 7. Находим раздел с уведомлениями и наводимя на него
        element = driver.find_element(By.XPATH, '/html/body/header/nav/div[2]/div[2]/nav/ul/li/a')
        ActionChains(driver).move_to_element(element).perform()
        time.sleep(0.1)

        # 8. Переходим в раздел с отправленными уведомлениями
        driver.find_element(By.XPATH, '/html/body/header/nav/div[2]/div[2]/nav/ul/li/ul/li[3]/a').click()

        # 9. Определяем количество страниц c результатами
        pages_info = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div[2]/p').text
        pages_num = int(re.findall(r'\d+', pages_info)[1]) + 1

        # 10. Итерируемся по страницам
        satisf_prompts = pd.DataFrame()
        for i in reversed(range(1, pages_num)):

            # 11. Ивзлекаем данные об отправленных уведомлениях
            driver.get(PROMPTS_URL + f"history/page/{i}")
            sent_prompts_object = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/table")
            sent_prompts = pd.read_html(sent_prompts_object.get_attribute('outerHTML'))[0]

            # 12. Форматируем время отправки
            sent_prompts['Sent from the server'] = pd.to_datetime(
                sent_prompts['Sent from the server'].str.replace(',', ''), format='%d.%m.%y %H:%M:%S')

            # 13. Оставляем только те записи, которые датируются заданным числом
            filtered_df = sent_prompts[
                (sent_prompts['Sent from the server'] >= DATETIME_START) &
                (sent_prompts['Sent from the server'] <= DATETIME_END)]

            # 14. Для каждого подходящего уведомления оставляем ID пользователя, а также дату и время
            filtered_df = filtered_df[['Participant ID', 'Title', 'Sent from the server']]
            filtered_df.columns = ['id', 'survey_name', 'sent_dt']

            # 15. Добавляем результаты в датасет
            satisf_prompts = pd.concat([filtered_df, satisf_prompts], ignore_index=True)

        # 16. Возвращаем датасает c подходящими уведомлениями
        satisf_prompts.to_excel('notifications.xlsx')
        return satisf_prompts

    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()