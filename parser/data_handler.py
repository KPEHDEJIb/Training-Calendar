import re
import json
from os import path, mkdir
from bs4 import BeautifulSoup


def save_data(data: dict):
    if not path.exists(path.abspath("../website")):
        mkdir(path.abspath("../website"))
    if not path.exists(path.abspath("../website/data")):
        mkdir(path.abspath("../website/data"))

    with open(path.abspath("../website/data/exercises.json"), 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def parse_data():
    days = ["Monday", "Wednesday", "Friday", "Saturday"]

    result = {"weeks": []}
    # Обрабатываем каждую неделю с 1-й по 12-ую (3 месяца)
    for i in range(1, 13):
        cur_week = {}

        with open(path.abspath(f"scraped_websites/index{i}.html"), 'r', encoding="utf-8") as f:
            src = f.read()
        soup = BeautifulSoup(src, "lxml")

        # Получение всех дней из всех недель в html
        items_days = [day.parent.parent.parent for day in soup.find_all(string=re.compile("НЕДЕЛЯ"))]

        # Получение данных из всех дней
        for j in range(len(items_days)):
            cur_week[days[j]] = {}
            # ==================== Общий список упражнений ====================
            # Получение списка всех упражнений с описанием
            for ex in list(items_days[j].find(string=re.compile(r"НЕДЕЛЯ")).parent.stripped_strings):
                cur_week[days[j]][ex.replace('\ufeff', '')] = None
            # ====================/Общий список упражнений ====================
            # Проверка на наличие описания подходов
            flag = False
            for ex in cur_week.keys():
                if "ЧАСТЬ" in ex:
                    flag = True
                    break
            if flag:
                break
            # ===================== Подходы и повторения ======================
            items_exercises = list(dict.fromkeys([k.parent for k in items_days[j].find_all(name="strong")]))
            # Удаление общего списка упражнений во избежание повторений
            for k in range(len(items_exercises)):
                if "НЕДЕЛЯ" in items_exercises[k].text:
                    items_exercises.pop(k)
                    break
            # Проход по каждому списку упражнений
            for k in range(len(items_exercises)):
                # Формирование полной строки с текстом
                text_list = list(items_exercises[k].stripped_strings)
                text = ' '.join(text_list).replace('\ufeff', '')

                # Поиск стартовой части для обрезания
                ex_name = ""
                for ex in cur_week[days[j]].keys():
                    cur_name = ex.replace('\ufeff', '').strip()
                    ex = cur_name.strip(" +")
                    if text.find(ex) != -1:
                        if ex_name in ex or not ex_name:
                            ex_name = ex

                # Обрезание
                if ex_name and (c := text.find(ex_name)) != -1:
                    t = text[c + len(ex_name):].strip().strip(" +")
                    cur_week[days[j]][ex_name] = t
            # =====================/Подходы и повторения ======================
        result["weeks"].append(cur_week)

    save_data(result)


def main():
    parse_data()


if __name__ == "__main__":
    main()
