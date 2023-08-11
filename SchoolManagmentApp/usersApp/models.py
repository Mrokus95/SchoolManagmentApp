from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from PIL import Image


class Profile(models.Model):
    TEACHER = "Teacher"
    PARENT = "Parent"
    STUDENT = "Student"
    ADMIN = "Admin"
    TYPE_ACCOUNT_CHOICES = [
        (TEACHER, "Teacher"),
        (PARENT, "Parent"),
        (STUDENT, "Student"),
        (ADMIN, "Admin"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to="users/avatars/", default="users/avatars/musk.webp"
    )
    phone_number = models.CharField(max_length=9, blank=True, null=True)
    account_type = models.CharField(
        max_length=10, choices=TYPE_ACCOUNT_CHOICES, default=STUDENT
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def validate_image(self, value):
        img = Image.open(value)
        if img.format not in ("JPEG", "JPG", "WEBP", "PNG"):
            raise ValidationError("Invalid image format")

    def clean(self):
        super().clean()

        if self.account_type not in [choice[0] for choice in self.TYPE_ACCOUNT_CHOICES]:
            raise ValidationError({"account_type": "Invalid account type"})

        if self.phone_number and len(self.phone_number) != 9:
            raise ValidationError(
                {"phone_number": "Phone number has to contain 9 digits"}
            )

        if self.phone_number and not self.phone_number.isdigit():
            raise ValidationError(
                {"phone_number": "Phone number can only contains digits."}
            )

        if self.photo:
            self.validate_image(self.photo)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ClassUnit(models.Model):
    start_year = models.IntegerField(
        validators=[
            MinValueValidator(2023),
        ],
        default=2023,
    )
    study_year = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)], default=1
    )
    letter_mark = models.CharField(
        max_length=1,
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
            ("E", "E"),
            ("F", "F"),
        ],
        null=False,
        blank=False,
    )

    class Meta:
        unique_together = ["start_year", "study_year", "letter_mark"]

    def __str__(self):
        return f"Class {self.study_year}{self.letter_mark}"


class Parent(models.Model):
    user = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="parent",
        limit_choices_to={"account_type": "Parent"},
    )

    def __str__(self):
        return (
            f"Parent: {self.user.user.first_name} {self.user.user.last_name}'s profile"
        )


class Student(models.Model):
    user = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="student",
        limit_choices_to={"account_type": "Student"},
    )
    class_unit = models.ForeignKey(
        ClassUnit, models.DO_NOTHING, related_name="students_in_class"
    )
    parent = models.ForeignKey(
        Parent, on_delete=models.CASCADE, related_name="children"
    )

    def __str__(self):
        return f"{self.user.user.first_name} {self.user.user.last_name} - student"
