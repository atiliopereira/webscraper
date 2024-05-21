from django.db import models


class Page(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=126)

    def __str__(self):
        return self.name or "-"


class Link(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=126)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("url", "page")

    def __str__(self):
        return self.name or "-"
