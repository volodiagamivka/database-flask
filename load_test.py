#!/usr/bin/env python3
import requests
import time
import threading
import random
from datetime import datetime
import sys

API_BASE_URL = "http://48.222.10.212:5000/api/v1"

class LoadGenerator:
    def __init__(self, base_url, num_threads=10, duration=300):
        self.base_url = base_url
        self.num_threads = num_threads
        self.duration = duration
        self.stop_flag = False
        self.request_count = 0
        self.error_count = 0
        self.lock = threading.Lock()
        
    def make_request(self, endpoint, method='GET', data=None):
        try:
            if method == 'GET':
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
            elif method == 'POST':
                response = requests.post(f"{self.base_url}{endpoint}", json=data, timeout=10)
            
            with self.lock:
                self.request_count += 1
                if response.status_code >= 400:
                    self.error_count += 1
            
            return response.status_code
        except Exception as e:
            with self.lock:
                self.error_count += 1
            return None
    
    def worker(self, worker_id):
        print(f"[{datetime.now()}] Worker {worker_id} started")
        
        while not self.stop_flag:
            endpoints = [
                ('/patients/', 'GET'),
                ('/hospitals/', 'GET'),
                ('/doctors/', 'GET'),
                ('/departments/', 'GET'),
            ]
            
            endpoint, method = random.choice(endpoints)
            status = self.make_request(endpoint, method)
            
            time.sleep(random.uniform(0.1, 0.5))
        
        print(f"[{datetime.now()}] Worker {worker_id} stopped")
    
    def monitor(self):
        start_time = time.time()
        last_count = 0
        
        while not self.stop_flag:
            time.sleep(10)
            elapsed = time.time() - start_time
            
            with self.lock:
                current_count = self.request_count
                errors = self.error_count
            
            rps = (current_count - last_count) / 10
            last_count = current_count
            
            print(f"\n{'='*60}")
            print(f"[{datetime.now()}] Статистика навантаження")
            print(f"{'='*60}")
            print(f"Час роботи: {elapsed:.1f}s")
            print(f"Всього запитів: {current_count}")
            print(f"Помилок: {errors}")
            print(f"RPS (запитів/сек): {rps:.2f}")
            print(f"Success rate: {((current_count - errors) / current_count * 100):.2f}%" if current_count > 0 else "N/A")
            print(f"{'='*60}\n")
            
            if elapsed >= self.duration:
                self.stop_flag = True
    
    def run(self):
        print(f"\n{'='*60}")
        print(f"🚀 Запуск генератора навантаження")
        print(f"{'='*60}")
        print(f"API URL: {self.base_url}")
        print(f"Кількість потоків: {self.num_threads}")
        print(f"Тривалість: {self.duration}s")
        print(f"{'='*60}\n")
        
        threads = []
        
        monitor_thread = threading.Thread(target=self.monitor)
        monitor_thread.start()
        
        for i in range(self.num_threads):
            thread = threading.Thread(target=self.worker, args=(i+1,))
            thread.start()
            threads.append(thread)
            time.sleep(0.1)
        
        for thread in threads:
            thread.join()
        
        monitor_thread.join()
        
        print(f"\n{'='*60}")
        print(f"✅ Тест завершено")
        print(f"{'='*60}")
        print(f"Всього запитів: {self.request_count}")
        print(f"Помилок: {self.error_count}")
        print(f"Success rate: {((self.request_count - self.error_count) / self.request_count * 100):.2f}%")
        print(f"{'='*60}\n")

def main():
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = API_BASE_URL
    
    num_threads = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    
    generator = LoadGenerator(base_url, num_threads, duration)
    
    try:
        generator.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Зупинка тесту...")
        generator.stop_flag = True
        time.sleep(2)

if __name__ == "__main__":
    main()

