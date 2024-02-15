from admin_ordering.models import OrderableModel
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from martor.models import MartorField
from solo.models import SingletonModel


class SideBarLink(OrderableModel):
    class Icon(models.TextChoices):
        BOX_TITLE = "box-title", "Naslov polja"
        EYE = "eye", "Oko"
        HANDSHAKE = "handshake", "Roka"

    landing_page = models.ForeignKey(
        "LandingPageConfig",
        on_delete=models.CASCADE,
        verbose_name="Domača stran",
    )

    gap = models.BooleanField(
        default=False,
        verbose_name="Presledek",
    )
    icon = models.CharField(
        max_length=100,
        choices=Icon.choices,
        default=Icon.HANDSHAKE,
        verbose_name="Ikona",
    )
    title = models.CharField(
        max_length=100,
        verbose_name="Naslov",
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Opis",
    )
    url = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        verbose_name="Povezava",
    )

    def __str__(self):
        return self.title

    class Meta(OrderableModel.Meta):
        verbose_name = "Povezava v stranski vrstici"
        verbose_name_plural = "Povezave v stranski vrstici"


class LandingPageConfig(SingletonModel):
    organizations = models.TextField(
        blank=True,
        verbose_name="Organizacije",
    )
    organizations_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Število organizacij",
    )

    def __str__(self):
        return "Domača stran"

    class Meta:
        verbose_name = "Domača stran"
        verbose_name_plural = "Domača stran"


class NewsItem(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Naslov",
    )
    publish_time = models.DateTimeField(
        verbose_name="Čas objave",
    )
    intro = MartorField(
        blank=True,
        null=True,
        verbose_name="Uvod",
    )
    content = MartorField(
        blank=True,
        null=True,
        verbose_name="Vsebina",
    )
    published = models.BooleanField(
        default=False,
        verbose_name="Objavljeno",
    )

    def get_absolute_url(self):
        return f"/new-home/novice/{self.id}/{slugify(self.title)}"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Novica"
        verbose_name_plural = "Novice"


class ContentPage(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Naslov",
    )
    content = MartorField(
        blank=True,
        null=True,
        verbose_name="Vsebina",
    )
    slug = models.SlugField(
        max_length=200,
        blank=True,
        verbose_name="Ključ za povezavo",
        help_text="Ime strani v povezavi (npr. glas-ljudstva.si/kljuc-za-povezavo, pusti prazno za samodejno generiranje ključa)",
    )
    published = models.BooleanField(
        default=False,
        verbose_name="Objavljeno",
    )

    def clean(self):
        if not self.slug:
            slug = slugify(self.title)
            while ContentPage.objects.filter(slug=slug).exists():
                slug = f"{slug}-1"
            self.slug = slug
        else:
            same_slug = ContentPage.objects.filter(slug=self.slug)
            if self.id:
                same_slug = same_slug.exclude(id=self.id)
            if same_slug.exists():
                raise ValidationError({"slug": "Ključ za povezavo mora biti unikaten."})

    def get_absolute_url(self):
        return f"/new-home/{self.slug}"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Vsebinska stran"
        verbose_name_plural = "Vsebinske strani"
