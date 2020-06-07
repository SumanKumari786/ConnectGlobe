from django.contrib import admin
from Globe.models import Feedback, MyProfile, Post, PostComment, Discussion

admin.site.site_header = ' ConnectGlobe Admin'
admin.site.site_title = 'ConnectGlobe Header'
admin.site.index_title = 'ConnectGlobe Models'

# Register your models here.
admin.site.register(Feedback)
admin.site.register(MyProfile)
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(Discussion)
