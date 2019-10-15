import urllib.request
import re

from django.http import request, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from bs4 import BeautifulSoup as bs

from .models import CourseModule


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
        return render(request, 'chapter.html', {
            'module_title': contents.title,
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
