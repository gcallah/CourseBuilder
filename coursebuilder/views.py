import urllib.request
import re
import random

from django.http import request, HttpResponseServerError, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from bs4 import BeautifulSoup as bs
from decimal import Decimal

from .models import CourseModule, ModuleSection, Question, Quiz, Grade


DEF_NUM_RAND_QS = 10 # total number of questins
site_hdr = "Generic Website"


def get_filenm(mod_nm):
    return mod_nm + '.html'


def landing_page(request: request) -> object:

    try:
        modules = CourseModule.objects.all().order_by('course_order')
        messageContent = "Course Modules"
        return render(request, 'landing_page.html', {
            'modules': modules,
            'header': site_hdr,
            'message': messageContent
        })
    except Exception:
        messageContent = "Database Not Connected"
        return render(request, 'landing_page.html', {
            'header': site_hdr,
            'message': messageContent
        })


def dynamic_about(request: request) -> object:
    try:
        return render(request, 'dynamic_about.html', {
            'header': site_hdr,
            'about': render_to_string('about.html'),
        })

    except Exception:
        return render(request, 'dynamic_about.html', {
            'header': site_hdr,
            'message': "Database Not Connected"
        })


def chapter(request, chapter='basics'):

    try:
        contents = CourseModule.objects.get(module=chapter)
        sections = ModuleSection.objects.filter(module=contents)\
            .order_by('order', 'lesson_order')
        rand_qs = get_quiz_question(contents)
        return render(request, 'chapter.html', {
            'module_title': contents.title,
            'sections': sections,
            'questions': rand_qs,
            'header': site_hdr,
            'content': contents.content,
            'mod_nm': chapter
        })
    except Exception:
        return render(request, 'chapter.html', {
            'header': site_hdr,
            'content': "Database Not Connected"})


def dynamic_gloss(request: request) -> object:
    try:
        return render(request, 'dynamic_gloss.html', {
            'header': site_hdr,
            'gloss': render_to_string('glossary.html'),
        })
    except Exception:
        return render(request, 'dynamic_gloss.html', {
            'header': site_hdr,
            'message': "Database Not Connected"
        })


@require_http_methods(["GET", "POST"])
def parse_search(request) -> object:

    def crawl_index(url):
        with urllib.request.urlopen(url) as response:
            html = response.read()
            html = bs(html, "html.parser")
            lst = bs.find_all(html, "a")
            url_lst = []
            for i in lst:
                web_url = i["href"]
                if "/coursebuilder/" in web_url:
                    url_lst.append(web_url)
            return url_lst

    def search_page(url_lst, query):
        result = []
        for i in url_lst:
            content_url = url + i
            with urllib.request.urlopen(content_url) as res:

                html = res.read()
                html = bs(html, "html.parser")
                strings = html.body.strings
                title = html.h1
                if title is None:
                    title = i.split("/")[-1]
                else:
                    title = re.sub("[\n]", "", title.string).strip()
                for i in strings:
                    i = re.sub("\n", " ", i)
                    if query in i.lower():
                        dic = {
                            "url": content_url,
                            "page": title,
                            "content": i
                        }
                        result.append(dic)
        return result

    url = "http://www.thecoursebuildercourse.com"

    try:
        header = "The coursebuilder Course"
        path = request.get_full_path()
        query = path.split("query=")[1]
        if("+") in query:
            query = " ".join(query.split("+")).lower()
        else:
            query = query.lower()

        data = search_page(crawl_index(url), query)

        return render(request,
                      'search.html', dict(data=data,
                                          header=header,
                                          query=query))
    except Exception as e:
        return HttpResponseServerError(e.__cause__,
                                       e.__context__,
                                       e.__traceback__)


def get_nav_links(curr_module, correct_pct, curr_quiz, mod_nm):
    nav_links = {}
    # show link to next module if it exists
    if curr_module is not None:
        nav_links = {
            'next': 'coursebuilder:' +
            curr_module.next_module
            if curr_module.next_module else False
        }
        # If user fails, show link to previous module
        if correct_pct < curr_quiz.minpass:
            nav_links['previous'] = 'coursebuilder:' + mod_nm
    return nav_links



def get_quiz_question(mod_nm):

    # Returns list of Randomized Questions
    # :param: mod_nm, module name
    # :return: list() containing randomized questions, mod_nm
    try:
        rand_qs = []
        questions = Question.objects.filter(module=mod_nm)
        total_num_questions = len(questions)
        num_qs_to_randomize = DEF_NUM_RAND_QS

        if total_num_questions > 0:
            # we have to fetch numq from here:
            quizzes = Quiz.objects.filter(module=mod_nm)

            # we should log if we get count > 1 here!
            for quiz in quizzes:
                # we should have only 1 if any!
                num_qs_to_randomize = quiz.numq
                break

            if total_num_questions >= num_qs_to_randomize:
                rand_qs = random.sample(list(questions), num_qs_to_randomize)
            else:
                rand_qs = random.sample(list(questions), total_num_questions)

        return rand_qs

        # And if we crashed along the way - we crash gracefully...
    except Exception:
        return render(request, 'chapter.html', {
            'header': site_hdr,
            'content': "Database Not Connected"})


def mark_quiz(user_answers, graded_answers):
    num_correct = 0

    for answered_question in user_answers:
        processed_answer = {}
        id_to_retrieve = next(iter(answered_question))
        original_question = get_object_or_404(Question, pk=id_to_retrieve)

        # Lets start building a dictionary
        # with the status for the particular questions.
        processed_answer['question'] = original_question.text
        processed_answer['correctAnswer'] = original_question.correct.lower()
        processed_answer['yourAnswer'] = answered_question[id_to_retrieve]

        correctanskey =\
            "answer{}".format(processed_answer['correctAnswer'].upper())
        youranskey =\
            "answer{}".format(processed_answer['yourAnswer'].upper())

        processed_answer['correctAnswerText'] =\
            getattr(original_question, correctanskey)
        processed_answer['yourAnswerText'] =\
            getattr(original_question, youranskey)

        # and now we are evaluating either as right or wrong...
        if answered_question[id_to_retrieve] ==\
                processed_answer['correctAnswer']:
            processed_answer['status'] = "right"
            num_correct += 1
        else:
            processed_answer['message'] = "Sorry, that's incorrect!"
            processed_answer['status'] = "wrong"
            # and store to ship to the Template.
        graded_answers.append(processed_answer)
    return num_correct


def grade_quiz(request):
    """
    :param request: request as HttpRequest()
    Returns an html page containing results of quiz.
    """
    try:
        num_rand_qs = DEF_NUM_RAND_QS
        # First, we process only when form is POSTed...
        if request.method == 'POST':
            graded_answers = []
            user_answers = []
            form_data = request.POST
            num_correct = 0

            # get only post fields containing user answers...
            for key, value in form_data.items():
                # what is going on here is completely obscure to me: GC
                if key.startswith('_'):
                    proper_id = str(key).strip('_')
                    user_answers.append({proper_id: value})

            # forces user to answer all quiz questions,
            # redirects to module page if not completed
            mod_nm = form_data['submit']
            contents = CourseModule.objects.get(module=mod_nm)
            questions = Question.objects.filter(module=contents)

            quizzes = Quiz.objects.filter(module=contents)
            # we should log if we get count > 1 here!
            for quiz in quizzes:
                num_rand_qs = quiz.numq
                show_answers = quiz.show_answers
                curr_quiz = quiz
                break

            num_qs_to_check = min(questions.count(), num_rand_qs)

            # Function to mark quiz
            num_correct = mark_quiz(user_answers, graded_answers)

            # Calculating quiz score
            correct_pct = Decimal((num_correct / num_qs_to_check) * 100)

            curr_module = None
            quiz_name = 'Quiz'
            modules = CourseModule.objects.get(module=mod_nm)
            # we should log if we get count > 1 here!
            # for this_module in modules:
            #     curr_module = this_module
            #     quiz_name = curr_module.title
            #     break
            curr_module = modules
            quiz_name = modules.title

            nav_links = get_nav_links(curr_module, correct_pct,
                                      curr_quiz, mod_nm)

            # now we are ready to record quiz results...
            if request.user.username != '':
                Grade.objects.create(participant=request.user,
                                     score=correct_pct.real,
                                     quiz=curr_quiz,
                                     quiz_name=mod_nm)

            # ok, all questions processed, lets render results...
            return render(request,
                          'graded_quiz.html',
                          dict(graded_answers=graded_answers,
                               num_ques=num_qs_to_check,
                               num_correct=num_correct,
                               correct_pct=int(correct_pct),
                               quiz_name=quiz_name,
                               show_answers=show_answers,
                               navigate_links=nav_links,
                               header=site_hdr))

        # If it is PUT, DELETE etc. we say we dont do that...
        else:
            return HttpResponseBadRequest("ERROR: Method not allowed")

    # And if we crashed along the way - we crash gracefully...
    except Exception as e:
        return HttpResponseServerError(e.__cause__,
                                       e.__context__,
                                       e.__traceback__)