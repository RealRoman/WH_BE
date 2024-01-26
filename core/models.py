from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.utils.translation import gettext_lazy as _l
from django.utils import timezone

def DO_NOTHING(collector, field, sub_objs, using):
    pass


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Update all instances pointing to this one
        related_fields = [field for field in self._meta.get_fields() if field.is_relation]
        for related_field in related_fields:
            related_instances = getattr(self, related_field.name).all()
            related_instances.update(is_active=self.is_active)

    class Meta:
        abstract = True



class Experience(BaseModel):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return f"{self.name} (ID {self.pk})"

    class Meta:
        verbose_name = "Expirience"
        verbose_name_plural = "Expirience"


class CertificationDifficulty(BaseModel):
    name = models.CharField(unique=True, max_length=25)

    def __str__(self) -> str:
        return f"{self.name}  (ID {self.pk})"

    class Meta:
        verbose_name = "Certification difficulty"
        verbose_name_plural = "Certification difficulty"


class Sports(BaseModel):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self) -> str:
        return f"{self.name} (ID {self.pk})"

    class Meta:
        verbose_name = "Sport"
        verbose_name_plural = "Sports"

class Certifications(BaseModel):
    name = models.CharField(unique=True, max_length=50)
    certification_difficulty = models.ForeignKey(CertificationDifficulty, on_delete=DO_NOTHING)
 
    def __str__(self) -> str:
        return f"{self.name} - {self.certification_difficulty.name} (ID {self.pk})"

    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"



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
    experience = models.ForeignKey(Experience, on_delete=DO_NOTHING, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_trainer = models.BooleanField(default=False)

    certification = models.ManyToManyField(
        Certifications,
        through='UserSportCertification',
    ),
    sport = models.ManyToManyField(
        Sports,
        through='UserSportCertification',
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class UserSportCertification(BaseModel):
    user = models.ForeignKey(User, on_delete=DO_NOTHING)
    sport = models.ForeignKey(Sports, on_delete=DO_NOTHING)
    certification = models.ForeignKey(Certifications, on_delete=DO_NOTHING)
   
    def __str__(self) -> str:
        return f"{self.user.email} - {self.sport.name} - {self.certification.name} (ID {self.pk})"

    class Meta:
        verbose_name = "User Sport Certification"
        verbose_name_plural = "User Sport Certification"



class Tags(BaseModel):
    name = models.CharField(unique=True, max_length=20)
    is_user_created = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=DO_NOTHING)
    sports = models.ManyToManyField(Sports, through='TagsSports')
   
    def __str__(self) -> str:
        return f"{self.name} (ID {self.pk})"
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class TagsSports(BaseModel):
    sport = models.ForeignKey(Sports, on_delete=DO_NOTHING)
    tag = models.ForeignKey(Tags, on_delete=DO_NOTHING)
   
    def __str__(self) -> str:
        return f"{self.sport.name} - {self.tag.name} (ID {self.pk})"
    
    class Meta:
        verbose_name = "Tags Sports"
        verbose_name_plural = "Tags Sports"


class Posts(BaseModel):
    content = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=DO_NOTHING)
    post = models.ForeignKey('self', null=True, on_delete=DO_NOTHING)
    tags = models.ManyToManyField(Tags, through='PostsTags')
    is_edited = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.content[:20]}... (ID {self.pk})"
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class PostsTags(BaseModel):
    post = models.ForeignKey(Posts, on_delete=DO_NOTHING)
    tag = models.ForeignKey(Tags, on_delete=DO_NOTHING)
 
    def __str__(self) -> str:
        return f"{self.tag.name} - {self.post.content[:20]}... (ID {self.pk})"

    class Meta:
        verbose_name = "Posts Tags"
        verbose_name_plural = "Posts Tags"


class Comments(BaseModel):
    content = models.CharField(max_length=250)
    post = models.ForeignKey(Posts, on_delete=DO_NOTHING)
    comment = models.ForeignKey('self', null=True, on_delete=DO_NOTHING)
    user = models.ForeignKey(User, on_delete=DO_NOTHING)
    is_edited = models.BooleanField(default=False)
   
    def __str__(self) -> str:
        return f"{self.user.email} - {self.content[:20]}... (ID {self.pk})"
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Likes(BaseModel):
    user = models.ForeignKey(User, on_delete=DO_NOTHING)
    post = models.ForeignKey(Posts, on_delete=DO_NOTHING)
    like = models.ForeignKey('self', null=True, on_delete=DO_NOTHING)
    

    def __str__(self) -> str:
        return f"Like (ID {self.pk})"
    
    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"















