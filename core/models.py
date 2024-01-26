from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.utils.translation import gettext_lazy as _l
from django.utils import timezone


def DO_NOTHING(collector, field, sub_objs, using):
    print('collector', collector)
    print('field', field)
    print('sub_objs', sub_objs)
    print('using', using)
    pass



class Experience(models.Model):
    name = models.CharField(max_length=25)


class CertificationDifficulty(models.Model):
    name = models.CharField(unique=True, max_length=25)


class Sports(models.Model):
    name = models.CharField(unique=True, max_length=50)

class Certification(models.Model):
    name = models.CharField(unique=True, max_length=50)
    certification_difficulty = models.ForeignKey(CertificationDifficulty, on_delete=DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserManager(BaseUserManager):
    def get_normalized_username(self, email):
        return self.model.normalize_username(email.split("@")[0])

    def create_user(
        self, email, password, is_staff=False, is_superuser=False, **extra_fields
    ):

        email = self.normalize_email(email)
        user = self.model(
            username=self.get_normalized_username(email),
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        return self.create_user(
            email=email, password=password, is_staff=True, is_superuser=True, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()


    USERNAME_FIELD = "email"

    email = models.EmailField(unique=True)
    username = models.CharField(
        verbose_name=_l("username"),
        max_length=30,
        blank=False,
        unique=True,
        error_messages={
            "unique": "Somebody already uses this username. How else do they call you? :)",
        },
    )
    first_name = models.CharField(verbose_name=_l("first name"), max_length=30, blank=False, null=False)
    last_name = models.CharField(verbose_name=_l("last name"), max_length=30, blank=False, null=False)
    state = models.CharField(max_length=5, null=True)
    city = models.CharField(max_length=25, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    experience = models.ForeignKey(Experience, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_trainer = models.BooleanField(default=False)

    certification = models.ManyToManyField(
        Certification,
        through='UserSportCertification',
    ),
    sport = models.ManyToManyField(
        Sports,
        through='UserSportCertification',
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class UserSportCertification(models.Model):
    user = models.ForeignKey(User, on_delete=DO_NOTHING)
    sport = models.ForeignKey(Sports, on_delete=DO_NOTHING)
    certification = models.ForeignKey(Certification, on_delete=DO_NOTHING)


class Tags(models.Model):
    name = models.CharField(unique=True, max_length=20)
    is_user_created = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=DO_NOTHING)
    sports = models.ManyToManyField(Sports, through='TagsSports')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TagsSports(models.Model):
    sport = models.ForeignKey(Sports, on_delete=DO_NOTHING)
    tag = models.ForeignKey(Tags, on_delete=DO_NOTHING)


class Posts(models.Model):
    content = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=DO_NOTHING)
    post = models.ForeignKey('self', null=True, on_delete=DO_NOTHING)
    tags = models.ManyToManyField(Tags, through='PostsTags')
    is_edited = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostsTags(models.Model):
    post = models.ForeignKey(Posts, on_delete=DO_NOTHING)
    tag = models.ForeignKey(Tags, on_delete=DO_NOTHING)


class Comments(models.Model):
    content = models.CharField(max_length=250)
    post = models.ForeignKey(Posts, on_delete=DO_NOTHING)
    comment = models.ForeignKey('self', null=True, on_delete=DO_NOTHING)
    user = models.ForeignKey(User, on_delete=DO_NOTHING)
    is_edited = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=DO_NOTHING)
    post = models.ForeignKey(Posts, on_delete=DO_NOTHING)
    like = models.ForeignKey('self', null=True, on_delete=DO_NOTHING)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)















