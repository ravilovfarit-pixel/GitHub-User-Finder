
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Имя файла для сохранения данных
DATA_FILE = "weather_data.json"

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary (Дневник погоды)")
        self.root.geometry("800x450")

        self.data = self.load_data()

        # --- Интерфейс (Пункт 1) ---
        
        # Левая панель для ввода данных
        input_frame = ttk.LabelFrame(root, text="Добавить новую запись")
        input_frame.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").pack(anchor="w", padx=5)
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.pack(fill="x", padx=5, pady=2)
        # Установка текущей даты по умолчанию
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(input_frame, text="Температура (°C):").pack(anchor="w", padx=5)
        self.temp_entry = ttk.Entry(input_frame)
        self.temp_entry.pack(fill="x", padx=5, pady=2)

        ttk.Label(input_frame, text="Описание погоды:").pack(anchor="w", padx=5)
        self.desc_entry = ttk.Entry(input_frame)
        self.desc_entry.pack(fill="x", padx=5, pady=2)

        self.precip_var = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="Осадки (есть/нет)", variable=self.precip_var).pack(anchor="w", padx=5, pady=5)

        # Кнопка добавления (Пункт 2)
        ttk.Button(input_frame, text="Добавить запись", command=self.add_entry).pack(fill="x", padx=5, pady=10)

        # Секция фильтрации (Пункт 3)
        filter_frame = ttk.LabelFrame(input_frame, text="Фильтрация")
        filter_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(filter_frame, text="Дата:").pack(anchor="w")
        self.filter_date = ttk.Entry(filter_frame)
        self.filter_date.pack(fill="x", pady=2)

        ttk.Label(filter_frame, text="Мин. темп (+10 и т.д.):").pack(anchor="w")
        self.filter_temp = ttk.Entry(filter_frame)
        self.filter_temp.pack(fill="x", pady=2)

        ttk.Button(filter_frame, text="Применить фильтр", command=self.update_table).pack(fill="x", pady=5)
        ttk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters).pack(fill="x")

        # Правая панель для таблицы (Пункт 2)
        table_frame = ttk.Frame(root)
        table_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        columns = ("date", "temp", "desc", "precip")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("temp", text="Темп. (°C)")
        self.tree.heading("desc", text="Описание")
        self.tree.heading("precip", text="Осадки")
        
        self.tree.column("temp", width=80)
        self.tree.column("precip", width=80)
        self.tree.pack(fill="both", expand=True)

        self.update_table()

    # --- Функционал ---

    def add_entry(self):
        # Проверка корректности (Пункт 5)
        date_str = self.date_entry.get().strip()
        temp_str = self.temp_entry.get().strip()
        desc = self.desc_entry.get().strip()
        precip = "Да" if self.precip_var.get() else "Нет"

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД")
            return

        try:
            temp = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом")
            return

        if not desc:
            messagebox.showerror("Ошибка", "Описание не должно быть пустым")
            return

        new_entry = {
            "date": date_str,
            "temp": temp,
            "desc": desc,
            "precip": precip
        }

        self.data.append(new_entry)
        self.save_data() # Сохранение в JSON (Пункт 4)
        self.update_table()
        
        # Очистка полей после ввода
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

    def update_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        f_date = self.filter_date.get().strip()
        f_temp = self.filter_temp.get().strip()

        for entry in self.data:
            # Логика фильтрации (Пункт 3)
            if f_date and entry["date"] != f_date:
                continue
            if f_temp:
                try:
                    if entry["temp"] < float(f_temp):
                        continue
                except ValueError:
                    pass

            self.tree.insert("", tk.END, values=(entry["date"], entry["temp"], entry["desc"], entry["precip"]))

    def reset_filters(self):
        self.filter_date.delete(0, tk.END)
        self.filter_temp.delete(0, tk.END)
        self.update_table()

    def save_data(self):
        """Пункт 4: Сохранение записей в JSON"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        """Пункт 4: Загрузка данных из JSON"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()
