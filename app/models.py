from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name: models.CharField = models.CharField(max_length=100, unique=True)
    description: models.TextField = models.TextField(blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'
    
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (ARCHIVED, 'Archived'),
    ]

    title: models.CharField = models.CharField(max_length=200)
    slug: models.SlugField = models.SlugField(max_length=200, unique=True)
    content: models.TextField = models.TextField()
    excerpt: models.TextField = models.TextField(max_length=300, blank=True)
    author: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category:models.ForeignKey = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags:models.ManyToManyField = models.ManyToManyField('Tag', blank=True, related_name='posts')
    status:models.CharField = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    featured_image:models.URLField = models.URLField(blank=True, null=True)
    is_featured:models.BooleanField = models.BooleanField(default=False)
    view_count:models.PositiveIntegerField = models.PositiveIntegerField(default=0)
    created_at:models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    published_at:models.DateTimeField = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['author', 'status']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name:models.CharField = models.CharField(max_length=50, unique=True)
    color:models.CharField = models.CharField(max_length=7, default='#007bff')  # Hex color code
    created_at:models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Comment(models.Model):
    post:models.ForeignKey = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author:models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    content:models.TextField = models.TextField()
    parent:models.ForeignKey = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_approved:models.BooleanField = models.BooleanField(default=True)
    created_at:models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'


class UserProfile(models.Model):
    user:models.OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio:models.TextField = models.TextField(max_length=500, blank=True)
    avatar:models.URLField = models.URLField(blank=True, null=True)
    website:models.URLField = models.URLField(blank=True, null=True)
    location:models.CharField = models.CharField(max_length=100, blank=True)
    birth_date:models.DateField = models.DateField(null=True, blank=True)
    is_verified:models.BooleanField = models.BooleanField(default=False)
    created_at:models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at:models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"