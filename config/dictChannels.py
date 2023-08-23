import os
CHANNELS_AZURE={
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(os.environ.get("REDISHOST"), os.environ.get("REDISPORT"))],
        },
    },
}

CHANNELS_LOCAL={
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}