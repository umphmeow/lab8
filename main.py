import random
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext


class BookRecommendationGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Book Recommendation")

        self.label = tk.Label(self.window, text="Введите количество книг:")
        self.label.pack()

        self.entry = tk.Entry(self.window)
        self.entry.pack()

        self.button = tk.Button(self.window, text="Сгенерировать", command=self.generate_recommendation)
        self.button.pack()

        self.output_text = scrolledtext.ScrolledText(self.window, height=10, width=50)
        self.output_text.pack()

    def generate_recommendation(self):
        try:
            k = int(self.entry.get())
            if k <= 0:
                messagebox.showerror("Ошибка", "Количество книг должно быть положительным числом.")
                return

            books = [{'title': f"Book{i + 1}"} for i in range(k)]

            all_book_sequences = self.read_books(books, k)
            self.output_text.insert(tk.END, "Все возможные последовательности чтения книг:\n")
            for sequence in all_book_sequences:
                self.output_text.insert(tk.END, f"{[book['title'] for book in sequence]}\n")

            books = self.rating_and_pages(books)

            self.output_text.insert(tk.END, "Список книг с присвоенными рейтингом и количеством страниц:\n")
            for book in books:
                self.output_text.insert(tk.END, f"{book}\n")

            filtered_sequences = self.print_filtered_sequences(books)
            if filtered_sequences:
                self.output_text.insert(tk.END,
                                        "Уникальные возможные последовательности книг для чтения после фильтрации:\n")
                for sequence in filtered_sequences:
                    avg_rating = sum([book['rating'] for book in sequence]) / len(sequence)
                    self.output_text.insert(tk.END,
                                            f"{[book['title'] for book in sequence]} Средний рейтинг: {avg_rating:.2f}\n")

                max_avg_rating = max(
                    [sum([book['rating'] for book in sequence]) / len(sequence) for sequence in filtered_sequences])
                self.output_text.insert(tk.END, f"Максимальный средний рейтинг: {max_avg_rating}\n")
            else:
                self.output_text.insert(tk.END,
                                        "В списке недостаточно книг для вычисления максимального среднего рейтинга.\n")

        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное количество книг.")

    def read_books(self, books, k, current=[], result=[]):
        if len(current) == k:
            result.append(current)
        else:
            for i in range(len(books)):
                if books[i] not in current:
                    self.read_books(books, k, current + [books[i]], result)
        return result

    def rating_and_pages(self, books):
        for book in books:
            rating = round(random.uniform(1.0, 5.0), 1)
            pages = random.randint(50, 500)
            book['rating'] = rating
            book['pages'] = pages
        return books

    def print_filtered_sequences(self, books):
        sequences = []
        for i in range(2, len(books) + 1):
            for sequence in self.get_permutations(books, i):
                sequence = list(sequence)
                for j in range(2, len(sequence)):
                    for k in range(j - 1, 0, -1):
                        if sequence[k]['rating'] < sequence[j]['rating']:
                            sequence[k + 1:j + 1] = sequence[k:j]
                            sequence[k] = sequence[j]
                            break
                if sequence not in sequences:
                    sequences.append(sequence)

        filtered_sequences = []
        for sequence in sequences:
            avg_rating = sum([book['rating'] for book in sequence]) / len(sequence)
            if avg_rating > 3.0:
                filtered_sequences.append(sequence)

        return filtered_sequences

    def get_permutations(self, books, r):
        if r == 0:
            return [[]]
        permutations = []
        for i in range(len(books)):
            for permutation in self.get_permutations(books[:i] + books[i + 1:], r - 1):
                permutations.append([books[i]] + permutation)
        return permutations

    def run(self):
        self.window.mainloop()

gui = BookRecommendationGUI()
gui.run()
