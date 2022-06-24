from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):  # наследуемся от класса Model
    name = models.CharField(max_length=255, unique=True)
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

    # обновить рейтинг автора
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.post_set = None

    def update_rating(self):
        # суммарный рейтинг всех комментариев к статьям
        sum_rating = self.post_set.aggregate(post_rating=Sum('post_rate'))
        result_sum_rating = 0
        try:
            result_sum_rating += sum_rating.get('post_rating')
        except TypeError:
            result_sum_rating = 0

        # суммарный рейтинг всех комментариев самого автора
        sum_comment_rating = self.author.comment_set.aggregate(comment_rating=Sum('comment_rate'))
        result_sum_comment_rating = 0
        result_sum_comment_rating += sum_comment_rating.get('comment_rating')

        # суммарный рейтинг каждой статьи автора умноженный на 3
        self.rate = result_sum_rating * 3 + result_sum_comment_rating
        # сохраняем результаты в базу данных
        self.save()


class Category(models.Model):
    article_category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    # связь один ко многим с Author
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # связь многие ко многим с Category
    post_category = models.ManyToManyField(Category)

    city = 'CI'
    politic = 'PO'
    economy = 'EC'
    sport = 'SP'
    culture = 'CU'
    technologies = 'TE'

    POSITIONS = [(city, ' Городские новости'),
                 (politic, 'Политика'),
                 (economy, 'Экономика'),
                 (sport, 'Спорт'),
                 (culture, 'Культура'),
                 (technologies, 'Технологии')]

    category = models.CharField(max_length=255,
                                choices=POSITIONS,
                                default=city)

    # дата и время создания поста
    date_created = models.DateField(auto_now_add=True)

    # заголовок статьи/новости
    title = models.CharField(max_length=50)

    # текст статьи/новости
    content = models.TextField()

    # рейтинг статьи/новости
    post_rate = models.IntegerField(default=0)

    # метод, увеличивающий рейтинг на единицу
    def like(self):
        self.post_rate += 1
        # сохранение значения в базу данных
        self.save()

    # метод, уменьшающий рейтин на единицу
    def dislike(self):
        self.post_rate -= 1
        # сохранение значения в базу данных
        self.save()

    # предварительный просмотр статьи (превью 124 символов статьи)
    def preview(self):
        return self.content[:125]

    # формат вывода наименования товара и его описания (первые 20 знаков)
    def __str__(self):
        return f'{self.title.title()}: {self.content[:20]}'


class PostCategory(models.Model):
    # связь «один ко многим» с моделью Post
    post_category = models.ForeignKey(Post, on_delete=models.CASCADE)
    # связь «один ко многим» с моделью Category
    category_category = models.ManyToManyField(Category)


class Comment(models.Model):
    # связь «один ко многим» с моделью Post
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # связь «один ко многим» с встроенной моделью User (комментарии может оставить любой пользователь)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    # текст комментария
    feedback_text = models.TextField()
    # дата и время создания комментария
    comment_date_created = models.DateField(auto_now_add=True)
    # рейтинг комментария
    comment_rate = models.IntegerField(default=0)

    # метод, увеличивающий рейтин на единицу
    def like(self):
        self.comment_rate += 1
        # сохранение значения в базу данных
        self.save()

    # метод, уменьшающий рейтин на единицу
    def dislike(self):
        self.comment_rate -= 1
        # сохранение значения в базу данных
        self.save()
