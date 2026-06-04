import psutil, os, time 
process = psutil.Process(os.getpid()) 
while True: 
    try: 
        mem = process.memory_info().rss / 1024 / 1024 
        cpu = process.cpu_percent(interval=0.1) 
        print(f"[Memory] Python Usage: {mem:.2f} MB | CPU: {cpu:.1f}%", end='\r') 
        time.sleep(1) 
    except KeyboardInterrupt: 
        break 
