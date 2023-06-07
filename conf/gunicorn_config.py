command = '/root/miniconda3/envs/webServerDjango/bin/gunicorn'
pythonpath = '/root/servidor/ceu-parasite-web/parasite_web'
bind = '127.0.0.1:8000'
workers = 3
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
debug = False
daemon = True
