from django.conf import settings

from redis import Redis

redis_client = Redis(host=settings.REDIS_HOST)
