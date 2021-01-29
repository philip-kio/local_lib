from django.db import models
from django.urls import reverse
import uuid #required  for  unique book instances
from django.contrib.auth.models import User
from datetime import date



# Create your models here.



class Genre(models.Model):
    '''Model representaing a book genre'''
    name= models.CharField(max_length =200, help_text='Enter a book genre (e.g Science Fiction)')


    def __str__(self):
        return self.name


class Language(models.Model):
    language= models.CharField(max_length=15, help_text='Enter the Language in which the books is written. e.g(English) ')

    def __str__(self):
        return self.language



class Book(models.Model):
    '''Model representing a book (but not a specific copy of a book)'''
    title = models.CharField(max_length= 200)
    # foreign key used because book can only have one autho, but authors can have many books

    author = models.ForeignKey('Author', on_delete = models.SET_NULL, null = True)
    summary = models.TextField(max_length=1000, help_text = 'Enter a bried description of the book')
    isbn = models.CharField('ISBN', max_length= 13, unique= True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a> ')


    #manytomanyfield used because a genere can contain many books. Books can cover many gnere.
    Genre = models.ManyToManyField(Genre, help_text = 'Select a genre for this book ')


    def display_genre(self):
        '''create a string for the Genre. This is required to display genre in Admin'''
        return ', '.join(genre.name for genre in self.Genre.all()[:3])
    display_genre.short_description = 'Genre'



    def __str__(self):
        # string representation of the object
        return self.title

    def get_absolute_url(self):
        # Returns the url to access a detaill record for this book
        return reverse('book-detail',kwargs={
            'pk': self.id
        })


class BookInstance(models.Model):
    '''Model reprensenting a specific copy of a book (i.e that can be borrowed from the library)'''
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, help_text ='Unique ID for this particular book across whole library' )
    book = models.ForeignKey('Book', on_delete = models.RESTRICT)
    imprint = models.CharField(max_length = 200)
    due_back = models.DateField(null= True, blank = True)



    LOAN_STATUS= (
        ('m', 'Maintainace'),
        ('o','On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length = 1,
        choices = LOAN_STATUS,
        blank= True,
        default = 'm',
        help_text = 'book availablity',
    )


    language = models.ForeignKey(
        Language,
        on_delete=models.RESTRICT,
    )

    borrower = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True )
    

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned', 'set book as returned'),)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        '''string representing the model object'''
        return f'{self.id} ({self.book.title}'



class Author(models.Model):
    '''model representing an author'''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length= 100)
    date_of_birth = models.DateField(null= True, blank= True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering =['last_name','first_name']


    def get_absolute_url(self):
        '''returns the url to access a particular author instance'''
        return reverse('author-detail', kwargs={
            'pk':self.id
        })




    def __str__(self):

        '''string for representing the model object'''
        return f'{self.last_name}, {self.first_name}'