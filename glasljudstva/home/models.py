from admin_ordering.models import OrderableModel
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from filer.fields.image import FilerImageField
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

    red = models.BooleanField(
        default=False,
        verbose_name="Rdeče",
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


class NavBarLink(OrderableModel):
    landing_page = models.ForeignKey(
        "LandingPageConfig",
        on_delete=models.CASCADE,
        verbose_name="Domača stran",
    )

    title = models.CharField(
        max_length=100,
        verbose_name="Naslov",
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
        abstract = True


class PrimaryNavBarLink(NavBarLink):
    class Meta(NavBarLink.Meta):
        verbose_name = "Povezava v glavni navigaciji"
        verbose_name_plural = "Povezave v glavni navigaciji"


class SecondaryNavBarLink(NavBarLink):
    class Meta(NavBarLink.Meta):
        verbose_name = "Povezava v sekundarni navigaciji"
        verbose_name_plural = "Povezave v sekundarni navigaciji"


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
        return f"/novice/{self.id}/{slugify(self.title)}"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Novica"
        verbose_name_plural = "Novice"


class CampaignItem(OrderableModel):
    title = models.CharField(
        max_length=200,
        verbose_name="Naslov",
    )
    image = FilerImageField(
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="campaign_image",
        verbose_name="Slika",
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
    promoted = models.BooleanField(
        default=False,
        verbose_name="Izpostavljeno na domači strani",
    )

    def get_absolute_url(self):
        return f"/kampanje/{self.id}/{slugify(self.title)}"

    def __str__(self):
        return self.title

    class Meta(OrderableModel.Meta):
        verbose_name = "Kampanja"
        verbose_name_plural = "Kampanje"


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
        return f"/objava/{self.slug}"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Vsebinska stran"
        verbose_name_plural = "Vsebinske strani"
