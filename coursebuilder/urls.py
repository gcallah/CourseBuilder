from django.conf.urls import url

from . import views

app_name = 'coursebuilder'  # type: str


def view_templ(vname):
    pass
    # we ought to be able to turn all of the code below into a single call


urlpatterns = [
    url(r'^$', views.landing_page, name='landing_page'),
    url(r'^coursebuilder/landing_page/',
        views.landing_page, name='landing_page'),
    url(r'^coursebuilder/chapter/(?P<chapter>\D+)/$',
        views.chapter, name='chapter'),
    url(r'^coursebuilder/dynamic_about/*$',
        views.dynamic_about, name='dynamic_about'),
    url(r'^coursebuilder/dynamic_gloss/*$',
        views.dynamic_gloss, name='dynamic_gloss'),
    url(r'^coursebuilder/parse_search/*$',
        views.parse_search, name='parse_search'),
    url(r'^coursebuilder/grade_quiz/*$', 
        views.grade_quiz, name='grade_quiz'),
    url(r'^coursebuilder/chapter/cb_models/',
        views.chapter,name='cb_models'),
    url(r'^coursebuilder/chapter/Intro/',
        views.chapter,name='Intro')
]
