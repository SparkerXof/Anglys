import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import threading
import anglys

class BlazePoseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Anglys")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Переменные для хранения путей
        self.video_path = tk.StringVar()
        self.model_path = tk.StringVar()
        self.output_video_path = tk.StringVar()
        self.output_pdf_path = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка весов столбцов
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Anglys", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # 1. Входное видео
        row = 1
        ttk.Label(main_frame, text="Входное видео:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.video_path, width=50).grid(row=row, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Обзор...", command=self.browse_video).grid(row=row, column=2, padx=5, pady=5)
        
        # 2. Модель BlazePose
        row += 1
        ttk.Label(main_frame, text="Модель BlazePose:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.model_path, width=50).grid(row=row, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Обзор...", command=self.browse_model).grid(row=row, column=2, padx=5, pady=5)
        
        # 3. Выходное видео
        row += 1
        ttk.Label(main_frame, text="Выходное видео:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_video_path, width=50).grid(row=row, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Сохранить как...", command=self.browse_output_video).grid(row=row, column=2, padx=5, pady=5)
        
        # 4. Выходной PDF
        row += 1
        ttk.Label(main_frame, text="Выходной PDF:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_pdf_path, width=50).grid(row=row, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Сохранить как...", command=self.browse_output_pdf).grid(row=row, column=2, padx=5, pady=5)
        
        # Кнопка запуска
        row += 1
        self.process_button = ttk.Button(main_frame, text="Начать обработку", 
                                         command=self.start_processing, style="Accent.TButton")
        self.process_button.grid(row=row, column=0, columnspan=3, pady=20)
        
        # Прогресс-бар
        row += 1
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Статус
        row += 1
        self.status_label = ttk.Label(main_frame, text="Готов к работе", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Текстовое поле для вывода консоли
        row += 1
        ttk.Label(main_frame, text="Вывод консоли:").grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(10,0))
        
        row += 1
        self.console_text = tk.Text(main_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.console_text.yview)
        self.console_text.configure(yscrollcommand=scrollbar.set)
        self.console_text.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        scrollbar.grid(row=row, column=2, sticky=(tk.N, tk.S), pady=5)
        
        # Настройка растягивания
        main_frame.rowconfigure(row, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
    def browse_video(self):
        filename = filedialog.askopenfilename(
            title="Выберите видеофайл",
            filetypes=[("Видео файлы", "*.mp4 *.avi *.mov *.mkv"), ("Все файлы", "*.*")]
        )
        if filename:
            self.video_path.set(filename)
            
    def browse_model(self):
        filename = filedialog.askopenfilename(
            title="Выберите файл модели BlazePose",
            filetypes=[("Модели", "*.task"), ("Все файлы", "*.*")]
        )
        if filename:
            self.model_path.set(filename)
            
    def browse_output_video(self):
        filename = filedialog.asksaveasfilename(
            title="Сохранить видео как",
            defaultextension=".mp4",
            filetypes=[("MP4 файлы", "*.mp4"), ("AVI файлы", "*.avi"), ("Все файлы", "*.*")]
        )
        if filename:
            self.output_video_path.set(filename)
            
    def browse_output_pdf(self):
        filename = filedialog.asksaveasfilename(
            title="Сохранить PDF как",
            defaultextension=".pdf",
            filetypes=[("PDF файлы", "*.pdf"), ("Все файлы", "*.*")]
        )
        if filename:
            self.output_pdf_path.set(filename)
            
    def update_console(self, text):
        """Добавление текста в консоль"""
        self.console_text.insert(tk.END, text)
        self.console_text.see(tk.END)
        self.root.update_idletasks()
        
    def run_processing(self):
        """Запуск обработки в отдельном потоке"""
        # Проверка заполнения полей
        if not all([self.video_path.get(), self.model_path.get(), 
                    self.output_video_path.get(), self.output_pdf_path.get()]):
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля!")
            self.progress.stop()
            self.progress.grid_remove()
            self.process_button.config(state="normal")
            self.status_label.config(text="Ошибка: не все поля заполнены")
            return
            
        # Проверка существования входных файлов
        if not os.path.exists(self.video_path.get()):
            messagebox.showerror("Ошибка", "Входное видео не найдено!")
            self.progress.stop()
            self.progress.grid_remove()
            self.process_button.config(state="normal")
            return
            
        if not os.path.exists(self.model_path.get()):
            messagebox.showerror("Ошибка", "Файл модели не найден!")
            self.progress.stop()
            self.progress.grid_remove()
            self.process_button.config(state="normal")
            return
        
        self.update_console("Начинаю обработку...\n")
        self.update_console("-" * 50 + "\n")
        
        try:
            # Запуск процесса
            anglys.main(self.video_path.get(), 
                        self.model_path.get(), 
                        self.output_video_path.get(), 
                        self.output_pdf_path.get())
                
        except Exception as e:
            error_msg = f"Ошибка: {str(e)}\n"
            self.update_console(error_msg)
            self.status_label.config(text="Ошибка выполнения")
            messagebox.showerror("Ошибка", f"Не удалось запустить процесс: {str(e)}")
            
        finally:
            self.progress.stop()
            self.progress.grid_remove()
            self.process_button.config(state="normal")

        self.update_console("Обработка завершена")
            
    def start_processing(self):
        """Запуск обработки в отдельном потоке"""
        # Очистка консоли
        self.console_text.delete(1.0, tk.END)
        
        # Блокировка кнопки и показ прогресса
        self.process_button.config(state="disabled")
        self.progress.grid()
        self.progress.start(10)
        self.status_label.config(text="Обработка...")
        
        # Запуск в отдельном потоке
        thread = threading.Thread(target=self.run_processing)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = BlazePoseGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()