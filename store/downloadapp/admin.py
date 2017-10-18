from django.contrib import admin

from downloadapp.models import Package
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(Package, MarkdownxModelAdmin)
