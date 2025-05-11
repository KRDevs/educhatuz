from django.db import models

from account.models.base_account import User, RoleChoices


class Rank(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Daraja"
        verbose_name_plural = "Darajalar"


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                limit_choices_to={'userRole': RoleChoices.TEACHER})
    name = models.CharField(max_length=255)
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "O'qituvchi"
        verbose_name_plural = "O'qituvchilar"

    def __str__(self):
        return self.user.username
