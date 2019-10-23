from unittest import skip

from autofixture import AutoFixture
from django.http import HttpResponseBadRequest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from coursebuilder.models import CourseModule, Quiz, Question, Grade

from .test_helpers import generate_form_data_for_quiz

class GradeQuizTestCase(TestCase):


    def setUp(self):
        """
        This method is called when you need to prepare
        some data to run your test.
        It is executed once in the beginning of the test case.
        """
        
        course_module = {
            # module_name : title
            "cb_models": "Course Builder Model",
            "cb_quiz" : "Course Builder Quiz"
        }

        self.num_questions_to_test = 10
        self.client = Client()

        modules_names = list(course_module.keys())
        index = 1
        for key, value in course_module.items():
            # create the course modules
            CourseModule.objects.create(
                module=key,
                title=value,
                content=value,
                next_module=modules_names[index%len(course_module)])
            index = index + 1

            Quiz.objects.create(
                module=CourseModule.objects.get(module=key),
                minpass=80,
                numq=self.num_questions_to_test)

            # creating temporary question for the modules
            fixture = AutoFixture(Question, generate_fk=True, field_values={
                'correct': 'a',
                'module': CourseModule.objects.get(module=key)
            })

            self.questions = fixture.create(self.num_questions_to_test,
                                            commit=True)

    def test_grade_quiz_except_POST_request_should_be_disallowed(self):
        temp = self.client.put(reverse('coursebuilder:grade_quiz'))
        self.assertEqual(temp.status_code, 400)

    def test_grade_quiz_should_be_used_right_template(self):
        quizzes = Quiz.objects.all()
        for quiz in quizzes:
            form_data = generate_form_data_for_quiz(quiz)
            
            # Send form_data in POST request...
            results = self.client.post(reverse('coursebuilder:grade_quiz'),
                                                data=form_data)
            self.assertEqual(results.status_code, 200)
            self.assertTemplateUsed(results, 'graded_quiz.html')