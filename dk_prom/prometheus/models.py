from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class Events(models.Model):
    title = models.CharField(verbose_name="Название события", max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.CharField(verbose_name="Описание события")
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Обложка")
    data = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    cost = models.DecimalField(decimal_places=2, max_digits=6, verbose_name="Цена")
    space = models.ForeignKey("Spaces", on_delete=models.PROTECT, verbose_name="Место")
    category = models.ForeignKey("Categories", on_delete=models.PROTECT, verbose_name="Категория")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event', kwargs={'event_slug': self.slug})

    class Meta:
        verbose_name = 'Афиша'
        verbose_name_plural = 'Афиша'
        ordering = ['data']


class Categories(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Spaces(models.Model):
    name = models.CharField(max_length=255, verbose_name="Место")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    capacity = models.IntegerField(verbose_name="Количество мест")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('space', kwargs={'space_slug': self.slug})

    class Meta:
        verbose_name = 'Пространство'
        verbose_name_plural = 'Пространства'
        ordering = ['id']


class Booking(models.Model):
    seats_reserved = models.IntegerField(verbose_name="Количество забронированных мест")
    time = models.DateTimeField(auto_now_add=True, verbose_name="Время бронирования")
    event = models.ForeignKey(Events, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('booking', kwargs={'book_id': self.pk})


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    post = models.TextField(blank=True, verbose_name="Пост")
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['time_create']


class FirstLessons(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    number = models.CharField(validators=[MinLengthValidator(11)], max_length=11, verbose_name="Номер телефона")
    group = models.ForeignKey("Groups", on_delete=models.CASCADE, verbose_name="Коллектив")

    def get_absolute_url(self):
        return reverse('record', kwargs={'record_id': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Запись в коллектив'
        verbose_name_plural = 'Записи в коллектив'
        ordering = ['id']


class Groups(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название коллектива")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    image1 = models.ImageField(upload_to="photos/group/", verbose_name="Фото 1")
    image2 = models.ImageField(upload_to="photos/group/", verbose_name="Фото 2")
    image3 = models.ImageField(upload_to="photos/group/", verbose_name="Фото 3")
    image4 = models.ImageField(upload_to="photos/group/", verbose_name="Фото 4")
    image5 = models.ImageField(upload_to="photos/group/", verbose_name="Фото 5")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group', kwargs={'group_slug': self.slug})

    class Meta:
        verbose_name = 'Коллектив'
        verbose_name_plural = 'Коллективы'
        ordering = ['id']
