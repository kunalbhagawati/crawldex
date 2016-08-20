import hashlib
from django.db import models


class MappingUrlTimestamp(models.Model):
    url = models.TextField()
    md5 = models.TextField()
    filename = models.TextField()
    indexed_timestamp = models.IntegerField()
    status_code = models.IntegerField()

    def save(self):
        # make md5 on url
        self.md5 = hashlib.md5(self.url.encode('utf-8')).hexdigest()
        return super().save()
