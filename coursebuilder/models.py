from django.db import models
from tinymce.models import HTMLField


MODNM_LEN = 16


class CourseModule(models.Model):
    """
    This table holds the modules (chapters) of our course.
    The content field should only have the intro material:
        the section contents go in the ModuleSection table.
    """
    course_order = models.IntegerField(blank=True, null=True)
    module = models.CharField(max_length=MODNM_LEN, unique=True)
    title = models.TextField()
    next_module = models.CharField(max_length=MODNM_LEN)
    content = HTMLField(default='Please enter your contents here!')

    def __str__(self):
        return self.title
