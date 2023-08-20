from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from ckeditor.fields import RichTextField  # Zengin metin düzenleme aracı için

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def blog_image_path(instance, filename):
    """Return a new filename for uploaded blog images in the format BLG-0000.extension."""
    # Get the extension of the file
    ext = filename.split('.')[-1]
    # Try to get the latest Blog's number to create a unique name
    try:
        latest_blog_number = int(Blog.objects.latest('id').id)
        blog_number = latest_blog_number + 1
    except Blog.DoesNotExist:
        blog_number = 1

    # Format the blog number to be 4 digits
    formatted_blog_number = f"{blog_number:04d}"
    
    # Return new filename
    return f'blog_photos/{formatted_blog_number}/BLG-{formatted_blog_number}.{ext}'



class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True, unique=True)
    featured = models.BooleanField(default=False)
    description = RichTextField()  # Zengin metin düzenleme aracı
    description_summary = models.TextField()
    photo = models.ImageField(upload_to=blog_image_path)
    date = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category, related_name="blogs")  # ManyToManyField
    comments = models.ManyToManyField('Comment', blank=True, related_name='blog_comments')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.featured:
            Blog.objects.filter(featured=True).exclude(id=self.id).update(featured=False)    
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    comment = models.TextField()
    
    def __str__(self):
        return f"{self.name} - {self.comment[:20]}..."

class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    reply = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.reply[:20]}..."



