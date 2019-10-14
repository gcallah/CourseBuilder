from django.contrib import admin

from .models import CourseModule
from .models import ModuleSection
from .models import Quiz
from .models import Question
from .models import Extras
from .models import Grade

admin.site.register(CourseModule)
admin.site.register(ModuleSection)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Extras)
admin.site.register(Grade)
