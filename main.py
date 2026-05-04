import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

# Файл для хранения избранных
FAVORITES_FILE = 'favorites.json'

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("400x500")

        # 1. Поле ввода
        tk.Label(root, text="Введите имя пользователя:").pack(pady=5)
        self.search_entry = tk.Entry(root, width=30)
        self.search_entry.pack(pady=5)

        # Кнопка поиска
        tk.Button(root, text="Найти", command=self.search_users).pack(pady=5)

        # 2. Список результатов
        tk.Label(root, text="Результаты:").pack(pady=5)
        self.results_list = tk.Listbox(root, width=50, height=10)
        self.results_list.pack(pady=5)

        # 3. Кнопка добавления в избранное
        tk.Button(root, text="Добавить в избранное", command=self.add_to_favorites).pack(pady=5)

    def search_users(self):
        username = self.search_entry.get().strip()
        
        # 5. Проверка корректности ввода
        if not username:
            messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым")
            return

        self.results_list.delete(0, tk.END)
        try:
            response = requests.get(f"https://github.com{username}")
            if response.status_code == 200:
                users = response.json().get('items', [])
                for user in users:
                    self.results_list.insert(tk.END, user['login'])
            else:
                messagebox.showerror("Ошибка API", "Не удалось получить данные")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def add_to_favorites(self):
        # 4. Сохранение в JSON
        selected = self.results_list.get(tk.ACTIVE)
        if not selected:
            return

        favorites = []
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, 'r') as f:
                favorites = json.load(f)

        if selected not in favorites:
            favorites.append(selected)
            with open(FAVORITES_FILE, 'w') as f:
                json.dump(favorites, f, indent=4)
            messagebox.showinfo("Успех", f"{selected} добавлен в избранное")
        else:
            messagebox.showinfo("Инфо", "Пользователь уже в списке")

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()
