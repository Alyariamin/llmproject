from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

class Tag(models.Model):
    title = models.CharField(max_length=255)
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title'] 

class Document(models.Model):
    STATUS_DRAFT = 'D'
    STATUS_PUBLISHED = 'P'
    STATUS_ARCHIVED = 'A'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_ARCHIVED, 'Archived'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    tag = models.ManyToManyField(Tag, related_name='documents',blank=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.status == self.STATUS_PUBLISHED:
            if not self.published_at:
                self.published_at = timezone.now()
        else:
            self.published_at = None

        if not self.summary and self.content:
            self.summary = self.content[:200] + "..."
        super().save(*args, **kwargs)

    class Meta:
        ordering =['title']

# models.py

class Survey(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True)
    
    documents = models.ManyToManyField(
        Document,
        related_name="surveys",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Survey #{self.id}"
    
