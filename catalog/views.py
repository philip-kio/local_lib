from django.shortcuts import render



from  .models import Book,BookInstance,Author,Genre
from django.views.generic import ListView,DetailView
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



import  datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm
# Create your views here.



@login_required
def index(request):
    '''
    view function for homepage of sites.
    '''
    # generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    

    # Count of Genres
    num_genre = Genre.objects.all().count()
    num_dev = Book.objects.filter(title__icontains='Django').count()





    # the all() is implied by default

    num_authors = Author.objects.count()

    # Number of visits to this view as counted in the session varaiable
    num_visits = request.session.get('num_visits',1)
    request.session['num_visits'] = num_visits + 1


    context = {
        'num_books':num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_dev': num_dev,
        'num_genre': num_genre,
        'num_visits':num_visits,
    }

    # Render the html template index.html with the data in the context variable
    return render(request, 'index.html', context= context)






class BookListView(ListView):
    model= Book
    template_name = 'book_list.html'
    paginate_by = 2



class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'


class AuthorListView(ListView):
    model= Author
    template_name = 'author_list.html'

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin,ListView):
    model = BookInstance
    template_name= 'book_instance_list_borrowed_user.html'

    paginate_by = 3


    def get_querryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_date')


class  BorrowedLibListView(PermissionRequiredMixin, ListView):
    model = BookInstance
    template_name = 'all_borrowers.html'
    permission_required = 'catalog.can_mark_returned'
    raise_exception = True





@login_required
@permission_required('catalog.can_mark_returned', raise_exception= True)
def renew_book_librarian(request,pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    # if this is a post request
    if request.method == 'POST':
        # check if the form is valid:
        form = RenewBookForm(request.POST)

        # check if the form is valid
        if form.is_valid():
            # process the data in form.cleaned_data as required 
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new url:
            return HttpResponseRedirect(reverse('librarian'))
    #  if this is a get
    else:
        proposed_renewal_date =datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial = {'renewal_date': proposed_renewal_date})

    context = {
         'form': form,
         'book_instance': book_instance,
    }
    return render(request,'catalog/book_renew_librarian.html',context)




from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

from .models import Author


class AuthorCreate(PermissionRequiredMixin,CreateView):
    model = Author
    fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'date_of_death'
        ]
    initial = {
            'date_of_death':'11/06/2021'
        }
    permission_required = 'catalog.can_mark_returned'
    


class AuthorDelete(PermissionRequiredMixin,DeleteView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    
    success_url = reverse_lazy('authors')

class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    
    fields ='__all__'
    success_url = reverse_lazy('author_detail')



class BookCreate(PermissionRequiredMixin,CreateView):
    model = Book
    fields= '__all__'
    permission_required = 'catalog.can_mark_returned'
    



class BookUpdate(PermissionRequiredMixin,UpdateView):
    model = Book
    fields= '__all__'
    permission_required = 'catalog.can_mark_returned'
    
 


class BookDelete(PermissionRequiredMixin,DeleteView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    
    success_url= reverse_lazy('books')


