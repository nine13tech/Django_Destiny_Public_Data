from django.contrib import admin
from .models import Milestones
from .models import Variants

admin.autodiscover()
admin.site.register(Milestones)
admin.site.register(Variants)
