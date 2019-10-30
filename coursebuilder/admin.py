from django.contrib import admin

from .models import CourseModule, ModuleSection, Quiz,\
    Question, Extras, Grade


class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ("module", "title", "course_order", "next_module")


class ModuleSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "order", "lesson_order")


class QuizAdmin(admin.ModelAdmin):
    list_display = ("module", "numq", "minpass", "show_answers")


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "module", "text", "difficulty", "qtype", "correct",
        "answerA", "answerB", "answerC", "answerD", "answerE"
    )


class GradeAdmin(admin.ModelAdmin):
    list_display = ("quiz", "score", "record_date", "participant", "quiz_name")


admin.site.register(CourseModule, CourseModuleAdmin)
admin.site.register(ModuleSection, ModuleSectionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Extras)
admin.site.register(Grade, GradeAdmin)
