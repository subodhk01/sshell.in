from django.db import models
from slugify import Slugify

slugify_text = Slugify()
slugify_text.to_lower = True
slugify_text.stop_words = ('a', 'an', 'the')
slugify_text.max_length = 200

def get_image_url(instance, filename):
    return f'blogs/{instance.slug}/{filename}'

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=230)
    date_created = models.DateField()
    title_image = models.ImageField(upload_to=get_image_url)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify_text(self.title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
