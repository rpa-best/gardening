from multiprocessing import cpu_count

bind = f'0.0.0.0:8008'
timeouts = 60
max_requests = 1000
workers = cpu_count()

reload = True
name = 'gardening_web'