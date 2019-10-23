from django.urls import reverse
from coursebuilder.models import CourseModule, Quiz, Question, Grade


def generate_form_data_for_quiz(quiz):
    
    quiz_questions = Question.objects.filter(module=quiz.module)
    
    form_data = {}
    for question in quiz_questions:
        form_data['_' + str(question.pk)] = question.correct
    
    form_data['submit'] = CourseModule.objects.get(title=quiz.module).module
    return form_data
                        