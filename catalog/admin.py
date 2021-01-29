from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language
# Register your models here.
 
 


# admin.site.register(Author)

class BookInline(admin.TabularInline):
    model = Book
    extra = 0

# Define the admin class 






class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name', 'date_of_birth','date_of_death')
    fields = ['first_name','last_name',('date_of_birth','date_of_death')]
    inlines = [BookInline]

# register the admin class with the associated model
admin.site.register(Author,AuthorAdmin)



# admin.site.register(Book)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

# define the admin class for BOok
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines= [BooksInstanceInline]





# admin.site.register(BookInstance)



@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter= ('status', 'due_back','language')
    fieldsets =(
        (None,{
            'fields':('book','imprint','id')
        }),
        ('Availability',{
            'fields':('status','due_back')
        }),
    )
    list_display = ('book','status','borrower', 'due_back', 'language','id')


admin.site.register(Genre)

admin.site.register(Language)