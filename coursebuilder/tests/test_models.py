from django.test import TestCase
from django.contrib.auth.models import User
from coursebuilder.models import QTYPES, CourseModule, ModuleSection, \
    Extras, Grade, Question, Quiz


def create_course_module():
    return CourseModule.objects.create(
        course_order=1,
        module="cb_module1",
        title="First Module",
        next_module="empty",
        content="<p>Welcome to the first module!<p>"
    )


def create_module_section(module):
    return ModuleSection.objects.create(
        module=module,
        title="First Lesson",
        order=1,
        lesson_order=1,
        content="<p>Welcome to the first lesson!<p>"
    )


def create_quiz(module):
    return Quiz.objects.create(
        module=module,
        minpass=75.0,
        numq=5,
        show_answers=True,
    )


def create_question(module):
    return Question.objects.create(
        module=module,
        text="Which of the following database does "
             "CourseBuilder use in the back-end?",
        difficulty=2,
        qtype=QTYPES[0],
        correct="B",
        answerA="MongoDB",
        answerB="SQLite",
        answerC="PostgreSQL"
    )


def create_extras():
    return Extras.objects.create(
        title="Extras",
        content="<p>Content for Extras<p>"
    )


def create_grade(quiz, participant):
    return Grade.objects.create(
        quiz=quiz,
        score=33.33,
        participant=participant,
        # record_date=date,
        quiz_name="Quiz for What Are Modules? How to Add Them?"
    )


class CourseModuleModelTest(TestCase):
    def test_create(self):
        module = create_course_module()
        self.assertTrue(isinstance(module, CourseModule))
        self.assertEqual(module.course_order, 1)
        self.assertEqual(module.module, "cb_module1")
        self.assertEqual(module.title, "First Module")
        self.assertEqual(module.next_module, "empty")
        self.assertEqual(module.content, "<p>Welcome to the first module!<p>")

    def test_get(self):
        module = create_course_module()
        response = CourseModule.objects.get(module="cb_module1")
        self.assertTrue(response.module, module.module)

    def test_delete(self):
        create_course_module()
        response = CourseModule.objects.filter(module="cb_module1").delete()
        self.assertIsNotNone(response)


class ModuleSectionModelTest(TestCase):
    def setUp(self):
        self.course_module = create_course_module()

    def test_create(self):
        module_section = create_module_section(self.course_module)
        self.assertTrue(isinstance(module_section, ModuleSection))
        self.assertEqual(module_section.module, self.course_module)
        self.assertEqual(module_section.title, "First Lesson")
        self.assertEqual(module_section.order, 1)
        self.assertEqual(module_section.lesson_order, 1)
        self.assertEqual(module_section.content,
                         "<p>Welcome to the first lesson!<p>")

    def test_get(self):
        module_section = create_module_section(self.course_module)
        response = ModuleSection.objects.get(title="First Lesson")
        self.assertTrue(response.title, module_section.title)

    def test_delete(self):
        create_module_section(self.course_module)
        response = ModuleSection.objects.filter(title="First Lesson").delete()
        self.assertIsNotNone(response)

    def tearDown(self):
        CourseModule.objects.all().delete()


class QuizModelTest(TestCase):
    def setUp(self):
        self.course_module = create_course_module()

    def test_create(self):
        quiz = create_quiz(self.course_module)
        self.assertTrue(isinstance(quiz, Quiz))
        self.assertEqual(quiz.module, self.course_module)
        self.assertEqual(quiz.minpass, 75.0)
        self.assertEqual(quiz.show_answers, True)

    def test_get(self):
        quiz = create_quiz(self.course_module)
        response = Quiz.objects.get(module=self.course_module)
        self.assertTrue(response.module, quiz.module)

    def test_delete(self):
        create_quiz(self.course_module)
        response = Quiz.objects.filter(module=self.course_module).delete()
        self.assertIsNotNone(response)

    def tearDown(self):
        CourseModule.objects.all().delete()


class QuestionModelTest(TestCase):
    def setUp(self):
        self.course_module = create_course_module()

    def test_create(self):
        question = create_question(self.course_module)
        self.assertTrue(isinstance(question, Question))
        self.assertEqual(question.module, self.course_module)
        self.assertEqual(question.text, "Which of the following database does "
                                        "CourseBuilder use in the back-end?")
        self.assertEqual(question.difficulty, 2)
        self.assertEqual(question.qtype, QTYPES[0])
        self.assertEqual(question.correct, "B")
        self.assertEqual(question.answerA, "MongoDB")
        self.assertEqual(question.answerB, "SQLite")
        self.assertEqual(question.answerC, "PostgreSQL")
        self.assertEqual(question.answerD, None)
        self.assertEqual(question.answerE, None)

    def test_get(self):
        question = create_question(self.course_module)
        response = Question.objects.get(module=self.course_module)
        self.assertTrue(response.module, question.module)

    def test_delete(self):
        create_question(self.course_module)
        response = Question.objects.filter(module=self.course_module).delete()
        self.assertIsNotNone(response)

    def tearDown(self):
        CourseModule.objects.all().delete()


class ExtrasModelTest(TestCase):
    def test_create(self):
        extras = create_extras()
        self.assertTrue(isinstance(extras, Extras))
        self.assertEqual(extras.title, "Extras")
        self.assertEqual(extras.content, "<p>Content for Extras<p>")

    def test_get(self):
        extras = create_extras()
        response = Extras.objects.get(title="Extras")
        self.assertTrue(response.title, extras.title)

    def test_delete(self):
        create_extras()
        response = Extras.objects.filter(title="Extras").delete()
        self.assertIsNotNone(response)


class GradeModelTest(TestCase):
    def setUp(self):
        self.course_module = create_course_module()
        self.participant = User.objects.create_user(
            'DevOps_team', 'devops', 'devops')
        self.quiz = create_quiz(self.course_module)

    def test_create(self):
        grade = create_grade(self.quiz, self.participant)
        self.assertTrue(isinstance(grade, Grade))
        self.assertEqual(grade.quiz, self.quiz)
        self.assertEqual(grade.participant, self.participant)
        self.assertEqual(grade.quiz_name,
                    "Quiz for What Are Modules? How to Add Them?")

    def test_get(self):
        grade = create_grade(self.quiz, self.participant)
        response = Grade.objects.get(quiz=self.quiz)
        self.assertTrue(response.score, grade.score)

    def test_delete(self):
        create_grade(self.quiz, self.participant)
        response = Grade.objects.filter(quiz=self.quiz).delete()
        self.assertIsNotNone(response)
