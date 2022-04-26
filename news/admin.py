from django.contrib import admin
from .models import News

# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(News, NewsAdmin)
