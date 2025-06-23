import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


class ProxyCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proxy Checker")
        self.root.geometry("800x600")

        # Переменные
        self.working_proxies = []
        self.dead_proxies = []
        self.total_proxies = 0

        # Создаем интерфейс
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для выбора файла
        file_frame = ttk.Frame(self.root, padding="10")
        file_frame.pack(fill=tk.X)

        ttk.Label(file_frame, text="Файл с прокси:").pack(side=tk.LEFT)
        self.file_entry = ttk.Entry(file_frame, width=50)
        self.file_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Обзор", command=self.browse_file).pack(side=tk.LEFT)

        # Выбор типа прокси
        type_frame = ttk.Frame(self.root, padding="10")
        type_frame.pack(fill=tk.X)

        ttk.Label(type_frame, text="Тип прокси:").pack(side=tk.LEFT)
        self.proxy_type = ttk.Combobox(type_frame, values=["HTTP", "HTTPS", "SOCKS4", "SOCKS5"])
        self.proxy_type.current(0)
        self.proxy_type.pack(side=tk.LEFT, padx=5)

        # Кнопки управления
        btn_frame = ttk.Frame(self.root, padding="10")
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="Начать проверку", command=self.start_checking).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Сохранить рабочие", command=self.save_working).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Очистить", command=self.clear_results).pack(side=tk.LEFT)

        # Прогресс-бар
        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X, padx=10, pady=5)

        # Результаты
        result_frame = ttk.Frame(self.root)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.results_text = tk.Text(result_frame, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Статистика
        self.stats_label = ttk.Label(self.root, text="Готов к проверке", relief=tk.SUNKEN)
        self.stats_label.pack(fill=tk.X, padx=10, pady=5)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)

    def start_checking(self):
        filename = self.file_entry.get()
        if not filename:
            messagebox.showerror("Ошибка", "Выберите файл с прокси!")
            return

        proxy_type = self.proxy_type.get()

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл: {e}")
            return

        if not proxies:
            messagebox.showerror("Ошибка", "Файл не содержит прокси!")
            return

        self.working_proxies = []
        self.dead_proxies = []
        self.total_proxies = len(proxies)
        self.progress['value'] = 0
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Начинаем проверку {self.total_proxies} прокси...\n")
        self.root.update()

        # Запускаем проверку в отдельном потоке
        self.run_check(proxies, proxy_type)

    def run_check(self, proxies, proxy_type):
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(self.check_proxy, proxy, proxy_type): proxy for proxy in proxies}

            for i, future in enumerate(as_completed(futures), 1):
                proxy = futures[future]
                try:
                    status, message = future.result()
                    if status:
                        self.working_proxies.append(proxy)
                        self.results_text.insert(tk.END, f"[{i}] ✅ Рабочий: {proxy} | {message}\n")
                    else:
                        self.dead_proxies.append(proxy)
                        self.results_text.insert(tk.END, f"[{i}] ❌ Не работает: {proxy} | {message}\n")

                    # Обновляем прогресс
                    progress = (i / self.total_proxies) * 100
                    self.progress['value'] = progress
                    self.stats_label.config(
                        text=f"Проверено: {i}/{self.total_proxies} | Рабочих: {len(self.working_proxies)} | Не рабочих: {len(self.dead_proxies)}")
                    self.root.update()

                    # Автопрокрутка
                    self.results_text.see(tk.END)
                except Exception as e:
                    self.dead_proxies.append(proxy)
                    self.results_text.insert(tk.END, f"[{i}] ❌ Ошибка проверки: {proxy} | {e}\n")

        # Показываем итоги
        self.results_text.insert(tk.END, "\n=== Проверка завершена ===\n")
        self.results_text.insert(tk.END, f"✅ Рабочих: {len(self.working_proxies)}\n")
        self.results_text.insert(tk.END, f"❌ Не рабочих: {len(self.dead_proxies)}\n")
        self.results_text.insert(tk.END,
                                 f"⚡ Эффективность: {int((len(self.working_proxies) / self.total_proxies) * 100)}%\n")

    def check_proxy(self, proxy, proxy_type):
        if '@' in proxy:
            creds, hostport = proxy.split('@', 1)
            host, port = hostport.split(':', 1)
            proxy_str = f"{creds}@{host}:{port}"
        else:
            host, port = proxy.split(':', 1)
            proxy_str = f"{host}:{port}"

        test_url = "http://httpbin.org/ip"
        proxies = {}

        try:
            if proxy_type == "HTTP":
                proxies = {"http": f"http://{proxy_str}", "https": f"http://{proxy_str}"}
            elif proxy_type == "HTTPS":
                proxies = {"http": f"https://{proxy_str}", "https": f"https://{proxy_str}"}
            elif proxy_type == "SOCKS4":
                proxies = {"http": f"socks4://{proxy_str}", "https": f"socks4://{proxy_str}"}
            elif proxy_type == "SOCKS5":
                proxies = {"http": f"socks5://{proxy_str}", "https": f"socks5://{proxy_str}"}

            start = time.time()
            response = requests.get(test_url, proxies=proxies, timeout=1)
            response.raise_for_status()
            latency = int((time.time() - start) * 1000)
            return True, f"Задержка: {latency}мс | Статус: {response.status_code}"

        except (requests.exceptions.ProxyError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                socket.gaierror,
                requests.exceptions.SSLError,
                requests.exceptions.ConnectionError) as e:
            error_msg = str(e)
            if '@' in proxy and proxy.split('@')[0] in error_msg:
                error_msg = error_msg.replace(proxy.split('@')[0], "***")
            return False, f"Ошибка: {error_msg}"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"

    def save_working(self):
        if not self.working_proxies:
            messagebox.showerror("Ошибка", "Нет рабочих прокси для сохранения!")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Сохранить рабочие прокси"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(self.working_proxies))
                messagebox.showinfo("Успех", f"Сохранено {len(self.working_proxies)} прокси в файл!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

    def clear_results(self):
        self.results_text.delete(1.0, tk.END)
        self.progress['value'] = 0
        self.stats_label.config(text="Готов к проверке")


if __name__ == "__main__":
    root = tk.Tk()
    app = ProxyCheckerApp(root)
    root.mainloop()