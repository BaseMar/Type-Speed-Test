import tkinter as tk
import random
import requests


class TypingTestApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Typing Speed Test')

        self.text = tk.StringVar()
        self.text.set('Click "Start" to begin the typing test')
        self.entry_text = tk.StringVar()
        self.entry_text.set('')
        self.test_duration = 60
        self.words_typed = []
        self.words_correct = 0
        self.words_incorrect = 0
        self.label_timer = tk.Label(self.master, text=f'Time remaining: {self.test_duration}', font=('Arial', 14))
        self.label_timer.pack(pady=10)
        self.timer_id = None

        self.label_text = tk.Label(self.master, textvariable=self.text, font=('Arial', 12))
        self.label_text.pack(pady=10)

        self.entry_word = tk.Entry(self.master, textvariable=self.entry_text, font=('Arial', 12))
        self.entry_word.pack(pady=10)
        self.entry_word.bind('<Return>', self.check_word)

        self.label_results = tk.Label(self.master, text='', font=('Arial', 12))
        self.label_results.pack(pady=10)

        self.button_start = tk.Button(self.master, text='Start', font=('Arial', 12), command=self.start_test)
        self.button_start.pack(pady=10)

        try:
            response = requests.get('https://random-word-api.herokuapp.com/all')
            response.raise_for_status()
            self.all_words=response.json()
        except (requests.exceptions.RequestException, ValueError):
            error_window = tk.Toplevel(self.master)
            error_label = tk.Label(error_window, text='Failed to retrieve word from API')
            error_label.pack(padx=10, pady=10)
            error_button = tk.Button(error_window, text='OK', command=error_window.destroy)
            error_button.pack(pady=10)
            self.master.wait_window(error_window)

    def start_test(self):
        self.time_remaining = self.test_duration
        self.words_typed = []
        self.text.set('')
        self.entry_word.config(state='normal')
        self.button_start.config(state='disabled')
        self.label_results.config(text='')
        self.entry_word.focus_set()
        self.update_text()
        self.timer_id = self.master.after(1000, self.countdown)

    def update_text(self, event=None):
        if self.time_remaining <= 0:
            self.entry_word.config(state='disabled')
            self.calculate_results()
            self.button_start.config(state='normal')
        else:
            self.text.set(self.get_next_word())
            self.entry_word.delete(0, 'end')
            self.label_results.config(text='')

    def get_next_word(self):
        return random.choice(self.all_words)

    def check_word(self, event):
        typed_word = self.entry_text.get().strip()
        expected_word = self.text.get().split()[-1].strip()
        self.words_typed.append(typed_word)
        self.entry_text.set('')
        if typed_word == expected_word:
            self.words_correct += 1
        else:
            self.words_incorrect += 1
        self.update_text()

    def calculate_results(self):
        self.entry_word.config(state='disabled')
        self.words_typed.append(self.entry_word.get())
        self.master.after_cancel(self.timer_id)
        total_words = len(self.words_typed)
        correct_words = self.words_correct
        incorrect_words = self.words_incorrect
        accuracy = correct_words / total_words * 100 if total_words > 0 else 100
        result_text = 'Total words typed: {}\n'.format(total_words)
        result_text += 'Correct words typed: {}\n'.format(correct_words)
        result_text += 'Incorrect words typed: {}\n'.format(incorrect_words)
        result_text += 'Accuracy: {:.2f}%\n'.format(accuracy)
        self.label_results.config(text=result_text)

    def countdown(self):
        self.time_remaining -= 1
        self.label_timer.config(text=f'Time remaining: {self.time_remaining}')
        if self.time_remaining > 0:
            self.timer_id = self.master.after(1000, self.countdown)
        else:
            self.update_text()

    def run(self):
        self.master.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    typing_test_app = TypingTestApp(root)
    typing_test_app.run()
