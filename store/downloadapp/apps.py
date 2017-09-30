from django.apps import AppConfig
from watson import search as watson

class DownloadappConfig(AppConfig):
    name = 'downloadapp'
    def ready(self):
        YourModel = self.get_model("Package")
        watson.register(YourModel.objects.filter(isPublished=True), fields=("name", "description",))
