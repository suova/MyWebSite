from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models import Count, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from ask_nkuznecova import settings


class TagsManager(models.Manager):
    def with_question_count(self):
        return self.annotate(questions_count=Count('question'))

    def order_by_question_count(self):
        return self.with_question_count().order_by('-questions_count')

    def order_by_name_with_question_count(self):
        return self.with_question_count().order_by('text')

    def get_popular_tags(self):
        return self.order_by_question_count().all()[:10]


class Tag(models.Model):
    text = models.CharField(max_length=50, verbose_name=u'Tag', unique=True)
    objects = TagsManager()
    def __unicode__(self):
        return self.text



class Profile(AbstractUser):
    avatar = models.ImageField(upload_to='static/img/', default="static/img/devochka-color.png")

@receiver(post_save, sender=User)
def new_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class QuestionManager(models.Manager):
    def newest(self):
        return self.order_by('-creation_time')
    def hot(self):
        return self.order_by('-rating')

    def tag_search(self, input_tag):
        return self.filter(tags__text=input_tag)

    def published(self):
        return self.filter(is_published=True)

    def user_questions(self, user_name):
        return self.filter(user__username=user_name)

    def date_search(self, date):
        return self.filter(date=date)




class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )
    creation_time = models.DateTimeField(default=timezone.now)
    objects = QuestionManager()

    def __unicode__(self):
        return self.title




class AnswerManager(models.Manager):
    def filter_question(self, q):
        return self.all().filter(question=q).order_by('rating', 'creation_time')


class Answer(models.Model):
    is_correct = models.BooleanField(default=False)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    creation_time = models.DateTimeField(default=timezone.now)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    objects = AnswerManager()

    def __unicode__(self):
        return self.text


class LikeDislikeManager(models.Manager): #Данный менеджер модели позволит забирать отдельно Like и Dislike
                                            # записи для текущего likedislike_set статьи или комментария.

    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name=("Голос"), choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Пользователь",on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # является сущностью, которая позволяет
                                                                # модели быть связанной с любыми другими моделями
    object_id = models.PositiveIntegerField() #содержит ID первичного ключа экземпляра модели, для которой
                                                # создаётся связь
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()

    def __unicode__(self):
        return unicode(self.value)



