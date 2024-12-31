from screeninfo import get_monitors

monitors = get_monitors()
print("모니터 정보:")

for idx, monitor in enumerate(monitors):
    print(f"{idx + 1}번째 모니터: {monitor.name}, Width: {monitor.width}, Height: {monitor.height}, Is primary: {monitor.is_primary}")