from coursebuilder.models import CourseModule, Question


def gen_quiz_form_data(quiz, running_id=None):
    quiz_questions = Question.objects.filter(module=quiz.module)
    form_data = {}

    if running_id is None:
        for question in quiz_questions:
            form_data['_' + str(question.pk)] = question.correct
        form_data['submit'] = CourseModule.objects.get(
            title=quiz.module).module
        return form_data
    answers_given = {}
    for question in quiz_questions:
        answer_status = ''
        if running_id % 2 == 0:
            form_data['_' + str(question.pk)] = question.correct
            answer_status = 'right'
        else:
            possible_answers = ['A', 'B', 'C', 'D', 'E']
            possible_answers.remove(question.correct.upper())
            form_data['_' + str(question.pk)] = possible_answers.pop()
            answer_status = 'wrong'
        # Now lets store given answer for future evaluation...
        status_record = {
            'answer_given': form_data['_' + str(question.pk)],
            'answer_status': answer_status
        }
        answers_given[question.text] = status_record
        running_id += 1

    # Send form_data in POST request...
    form_data['submit'] = CourseModule.objects.get(title=quiz.module).module
    return form_data, answers_given
