from parasite_web.celery import app as celery_app

@celery_app.task
def say_hi():
    print("HI")
