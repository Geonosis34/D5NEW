from django.db import models

class News(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    author = models.CharField(max_length=50)
    dateCreation = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return f'/news/{self.id}'

    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='news',
    )
    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'