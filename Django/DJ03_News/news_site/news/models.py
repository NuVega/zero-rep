from django.db import models

from django.db import models

class NewsPost(models.Model):
    title = models.CharField('Название новости', max_length=100)
    short_description = models.CharField('Краткое описание', max_length=300)
    text = models.TextField('Текст новости')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.CharField('Автор', max_length=100)

    def __str__(self):
        return f"{self.title} ({self.author})"
