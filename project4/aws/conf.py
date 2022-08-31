AWS_S3_HOST = 's3.ca-central-1.amazonaws.com'
AWS_ACCESS_KEY_ID = 'AKIAZHCVDPUKBB2LK6WD'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'django-greensky-bucket'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'