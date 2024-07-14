from datetime import timedelta

try:
    from celery import Task
except:
    # fallback
    Task = object
    
try:
    from huey.contrib.djhuey import periodic_task
except:
    # https://github.com/coleifer/huey/blob/0b6722a64f408d7d4b37a8eb8b38fa24aa61f5de/huey/contrib/mini.py#L69C1-L72C25
    def periodic_task(self, validate_func):
        def decorator(fn):
            return self.task(validate_func)(fn)
        return decorator

from static_sitemaps import conf
from static_sitemaps.generator import SitemapGenerator

def loop_x_minutes(minutes=60):
    def validate_date(timestamp):
        return timestamp.second % seconds == 0
    return validate_date
    
@periodic_task(loop_x_minutes())
def generate_sitemap_task(number):
    generator = SitemapGenerator(verbosity=1)
    generator.write()

__author__ = 'xaralis'

# Create class conditionally so the task can be bypassed when repetition 
# is set to something which evaluates to False.
if conf.CELERY_TASK_REPETITION:
    class GenerateSitemap(Task):
        run_every = timedelta(minutes=conf.CELERY_TASK_REPETITION)
    
        def run(self, **kwargs):
            generator = SitemapGenerator(verbosity=1)
            generator.write()

