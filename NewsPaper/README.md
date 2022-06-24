# NewsPaper5.9
1. >>> from news.models import User
>>> user1 = User.objects.create_user('Skill Factor')
>>> user2 = User.objects.create_user('Box Movier')

3.>>> from news.models import Category
>>> Category.objects.create(article_category = 'sport')
<Category: Category object (1)>
>>> Category.objects.create(article_category='culture')
<Category: Category object (2)>
>>> Category.objects.create(article_category='politic')
<Category: Category object (3)>
>>> Category.objects.create(article_category='technologies')
<Category: Category object (4)>


