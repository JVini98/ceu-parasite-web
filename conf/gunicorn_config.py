command = '/root/miniconda3/envs/webServerDjango/bin/gunicorn'
pythonpath = '/root/servidor/ceu-parasite-web/parasite_web'
bind = '0.0.0.0:8000'
workers = 3
daemon = True
