from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('removed', 'Removed'),
    ]

    title = models.CharField(max_length=255)
    author = models.ManyToManyField(Author, related_name='books')
    genre = models.ManyToManyField(Genre, related_name='books', blank=True)
    cover = models.TextField(blank=True, null=True, default='https://shorturl.at/HIdup')
    publication_date = models.DateField(blank=True, null=True)
    add_date = models.DateField(auto_now_add=True)
    synopsis = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, default='I love reading!')
    pfp = models.TextField(blank=True, null=True, default='https://shorturl.at/QYuov')

    def __str__(self):
        return self.user.username

class Review(models.Model):
    STATUS_CHOICES = [
        ('ok', 'OK'),
        ('hidden', 'Hidden'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ok')

class Shelf(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='shelves')
    name = models.CharField(max_length=50, default="My Shelf")

class ShelfBook(models.Model):
    STATUS_CHOICES = [
        ('want', 'Want to read'),
        ('reading', 'Currently reading'),
        ('read', 'Already read')
    ]

    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    book = models.ManyToManyField(Book, related_name='shelfbook')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)
