from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class PurBeurreAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Missing email")

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("Missing email")

        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class PurBeurreUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = PurBeurreAccountManager()

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer : All superusers are staff
        return self.is_admin

    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(package_name):
        return True


class Product(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__similarity_value = 0
        self.__saved = False

    code = models.TextField(primary_key=True)
    name = models.TextField()

    nutrition_score = models.IntegerField()
    nutrition_grade = models.CharField(max_length=1)

    quantity = models.TextField()

    energy_100g = models.IntegerField()
    energy_unit = models.TextField()
    carbohydrates_100g = models.FloatField()
    sugars_100g = models.FloatField()
    fat_100g = models.FloatField()
    saturated_fat_100g = models.FloatField()
    salt_100g = models.FloatField()
    sodium_100g = models.FloatField()
    fiber_100g = models.FloatField()
    proteins_100g = models.FloatField()

    thumbnail_url = models.TextField()

    @property
    def display_name(self):
        return f"{self.name}, {self.quantity}"

    @property
    def kcal(self):
        if self.energy_unit.lower() == "kj":
            return round(self.energy_100g / 4.184)

        return self.energy_100g

    @property
    def similarity(self):
        return self.__similarity_value

    @similarity.setter
    def similarity(self, value):
        self.__similarity_value = value

    @property
    def saved(self):
        return self.__saved

    @saved.setter
    def saved(self, value):
        self.__saved = value


class Category(models.Model):
    code = models.TextField(primary_key=True)
    name = models.TextField()


class CategoryProduct(models.Model):
    class Meta:
        unique_together = [['category', 'product']]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class UserProduct(models.Model):
    class Meta:
        unique_together = [['user', 'product', 'substitute']]

    user = models.ForeignKey(PurBeurreUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="product", on_delete=models.CASCADE)
    substitute = models.ForeignKey(Product, related_name="substitute", on_delete=models.CASCADE)
