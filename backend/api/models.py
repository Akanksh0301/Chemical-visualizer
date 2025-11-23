from django.db import models
import json

class Dataset(models.Model):
    original_filename = models.CharField(max_length=255)
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    row_count = models.IntegerField(default=0)
    summary_json = models.TextField(default='{}')

    def set_summary(self, summary_dict):
        self.summary_json = json.dumps(summary_dict)

    def get_summary(self):
        try:
            return json.loads(self.summary_json)
        except:
            return {}
