import tkinter as tk
from tkinter import messagebox
import requests
import json
import os
import re

# Файл для хранения избранных
FAVORITES_FILE = 'favorites.json'

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("400x550")

        # 1. Поле ввода
        tk.Label(root, text="Введите имя пользователя:").pack(pady=5)
        self.search_entry = tk.Entry(root, width=30)
        self.search_entry.pack(pady=5)

        # Кнопка поиска
        tk.Button(root, text="Найти", command=self.search_users).pack(pady=5)

        # 2. Список результатов
        tk.Label(root, text="Результаты:").pack(pady=5)
        self.results_list = tk.Listbox(root, width=50, height=10)
        self.results_list.pack(pady=10, padx=10)

        # 3. Кнопка добавления в избранное
        tk.Button(root, text="Добавить в избранное", command=self.add_to_favorites, bg="#e1e1e1").pack(pady=5)

    def search_users(self):
        query = self.search_entry.get().strip()
        
        # Валидация: пустое поле и допустимые символы (для GitHub это латиница, цифры и дефис)
        if not query:
            messagebox.showwarning("Внимание", "Поле поиска не должно быть пустым")
            return
        
        if not re.match(r"^[a-zA-Z0-9-]*$", query):
            messagebox.showwarning("Ошибка ввода", "Используйте только латиницу, цифры и дефис")
            return

        self.results_list.delete(0, tk.END)
        
        try:
            # ИСПРАВЛЕНО: правильный URL API для поиска пользователей
            url = f"https://github.com{query}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                users = data.get('items', [])
                
                if not users:
                    self.results_list.insert(tk.END, "Пользователи не найдены")
                else:
                    for user in users:
                        self.results_list.insert(tk.END, user['login'])
            
            elif response.status_code == 403:
                messagebox.showerror("Лимит запросов", "Превышен лимит запросов API. Подождите немного.")
            else:
                messagebox.showerror("Ошибка API", f"Ошибка сервера: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка сети", "Проверьте интернет-соединение")

    def add_to_favorites(self):
        selected = self.results_list.get(tk.ACTIVE)
        
        # Проверка, что выбрано имя пользователя, а не сообщение об ошибке
        if not selected or selected == "Пользователи не найдены":
            messagebox.showwarning("Выбор", "Сначала выберите пользователя из списка")
            return

        favorites = []
        
        # ИСПРАВЛЕНО: Безопасное чтение JSON с обработкой исключений
        try:
            if os.path.exists(FAVORITES_FILE):
                with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
                    favorites = json.load(f)
        except (json.JSONDecodeError, IOError):
            favorites = [] # Если файл поврежден, начинаем со пустого списка

        if selected not in favorites:
            favorites.append(selected)
            try:
                with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(favorites, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("Успех", f"{selected} добавлен в избранное")
            except IOError as e:
                messagebox.showerror("Ошибка записи", f"Не удалось сохранить файл: {e}")
        else:
            messagebox.showinfo("Инфо", "Пользователь уже в списке")

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()
