from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display=('userid', 'email', 'username', 'password', 'avatar')

class CorpusAdmin(admin.ModelAdmin):
    list_display=('uuid', 'userid', 'timestamp', 'first_couplet', 'second_couplet', 'quality', 'status')

admin.site.register(User, UserAdmin)
admin.site.register(Corpus, CorpusAdmin)