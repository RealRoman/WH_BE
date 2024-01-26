from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    Experience,
    Posts,
    Comments,
    Likes,
    Tags,
    Certifications,
    CertificationDifficulty,
    UserSportCertification,
    TagsSports,
    PostsTags,
    Sports
)
from django.contrib.auth.models import Group

admin.site.unregister(Group)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "pk",
        "email",
        "username",
        "is_active",
        "is_trainer",
        "created_at",
    )
    list_filter = ("is_active",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email", "state", "city", "latitude", "longitude")}),
        (
            ("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_trainer"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "username",
                    "first_name",
                    "last_name",
                    "state", 
                    "city", 
                    "latitude", 
                    "longitude",
                    "is_active",
                    "is_staff", 
                    "is_trainer", 
                ),
            },
        ),
    )

    def has_delete_permission(self, request, obj=None):
        return False 


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "is_active"
    )

    list_filter = ("is_active",)

    def has_delete_permission(self, request, obj=None):
        return False
    

@admin.register(CertificationDifficulty)
class CertificationDifficultyAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "is_active"
    )

    list_filter = ("is_active",)

    def has_delete_permission(self, request, obj=None):
        return False
    

@admin.register(Sports)
class SportsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "is_active",
        "created_at"
    )

    list_filter = ("name", "is_active",)

    def has_delete_permission(self, request, obj=None):
        return False
       

@admin.register(Certifications)
class CertificationsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "certification_difficulty",
        "created_at",
        "is_active"
    )

    list_filter = ("is_active",)

    def has_delete_permission(self, request, obj=None):
        return False 
           

@admin.register(UserSportCertification)
class UserSportCertificationAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "sport",
        "certification",
        "created_at",
        "is_active"
    )

    list_filter = ("is_active",)

    def has_delete_permission(self, request, obj=None):
        return False 
               

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "created_at",
        "is_active"
    )

    list_filter = ("name", "sports", "is_active",)

    def has_delete_permission(self, request, obj=None):
        return False 
                   

@admin.register(TagsSports)
class TagsSportsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "sport",
        "tag",
        "created_at",
        "is_active"
    )

    list_filter = ("sport", "tag", "is_active",)

    def has_delete_permission(self, request, obj=None):
        return False 
    
                   
@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "content",
        "post",
        "is_edited",
        "is_active",
        "created_at"
    )

    list_filter = ("user", "content", "post", "is_active",)

    def has_delete_permission(self, request, obj=None):
        return False 
    
                   
@admin.register(PostsTags)
class PostsTagsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "post",
        "tag",
    )

    list_filter = ("post", "tag", "post", "is_active",)

    def has_delete_permission(self, request, obj=None):
        return False 
        
                   
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "content",
        "post",
        "is_edited",
        "is_active",
        "created_at"
    )

    list_filter = ("user", "content", "post", "is_active",)

    def has_delete_permission(self, request, obj=None):
        return False 
            
                   
@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "post",
        "like",
        "is_active",
        "created_at"
    )

    list_filter = ("user", "like", "post", "is_active",)

    def has_delete_permission(self, request, obj=None):
        return False 