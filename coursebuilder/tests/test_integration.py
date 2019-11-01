#!/usr/bin/env python
"""Tests for CourseBuilder code"""
from autofixture import AutoFixture
from django.test import TestCase, Client
from django.urls import reverse

from coursebuilder.models import CourseModule, Quiz, Question
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
            "cb_quiz": "Course Builder Quiz"
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
                next_module=modules_names[index % len(course_module)])
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
            results = self.client.post(
                reverse('coursebuilder:grade_quiz'), data=form_data)
            self.assertEqual(results.status_code, 200)
            self.assertTemplateUsed(results, 'graded_quiz.html')

    def test_grade_quiz_all_answers_should_be_graded(self):
        quizzes = Quiz.objects.all()
        for quiz in quizzes:
            form_data = generate_form_data_for_quiz(quiz)
            # Send form_data in POST request...
            results = self.client.post(
                reverse('coursebuilder:grade_quiz'), data=form_data)
            graded_answers = results.context['graded_answers']
            self.assertEqual(len(graded_answers), self.num_questions_to_test)

    def test_grade_quiz_html_content_should_be_corrected(self):
        quizzes = Quiz.objects.all()
        for quiz in quizzes:
            form_data = generate_form_data_for_quiz(quiz)
            # Send form_data in POST request...
            results = self.client.post(
                reverse('coursebuilder:grade_quiz'), data=form_data)
            # Did we counter results right?
            correct_answers = results.context['num_correct']
            expected_message = \
                "<span>You have correctly answered {0} out of {1} " \
                "questions giving you a score of 100%.</span>"\
                .format(str(correct_answers),
                        str(self.num_questions_to_test))

            self.assertInHTML(expected_message, str(results.content))

    def test_quiz_displays_answers(self):
        # get all Quizzes...
        """
        Integration test for DC-5 Display correct answers.
        Check is returned graded_answers
        done right work evaluating right & wrong.
        """
        quizzes = Quiz.objects.all()
        # running_id = 0
        # for each of the Quizzes lets try to answer it...
        for quiz in quizzes:
            # get all questions & Generate form_data with the right answers...

            # Send form_data in POST request...
            form_data, answers_given = generate_form_data_for_quiz(
                                        quiz, running_id=0)
            results = self.client.post(reverse('coursebuilder:grade_quiz'),
                                       data=form_data)

            # Lets get evaluation results...
            graded_answers = results.context['graded_answers']

            # Did all answers were graded?
            self.assertEqual(len(graded_answers), self.num_questions_to_test)

            # Did we got all the messages right?..
            for graded_answer in graded_answers:
                # Find this question in given answer...
                specimen = answers_given[graded_answer['question']]
                # Check what answer was given
                # and does it match right one & assert that they match...
                self.assertEqual(specimen['answer_status'],
                                 graded_answer['status'])
