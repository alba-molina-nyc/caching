from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Memo, MemoItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import OrderForm

# Create your views here.
from django.http import HttpResponse

# create private function from this request we are going to take the memo.id
def _memo_id(request):
    # session_key -> session_id,
    memo = request.session.session_key
    if not memo:
        memo = request.session.create()
    # return the memo & memo id
    return memo

# decrement and remove memoItem aka job by 1
def remove_memo_item(request, job_id):
    memo = Memo.objects.get(memo_id=_memo_id(request))
    job = get_object_or_404(Job, id=job_id)
    memo_item = MemoItem.objects.get(job=job, memo=memo)
    memo_item.delete()
    return redirect('memo')

# add job inside the memo, so need job_id
def add_memo(request, job_id):
    job = Job.objects.get(id=job_id) #get the job
    try: 
        memo = Memo.objects.get(memo_id=_memo_id(request)) # the memo using the memo_id present in the session
    except Memo.DoesNotExist:
        memo = Memo.objects.create(
            memo_id = _memo_id(request)
        )
    memo.save() # up to this point we have a job and the cart put the job inside the cart, the job becomes cartItem

    try:
        memo_item = MemoItem.objects.get(job=job, memo=memo)
        memo_item.quantity += 1 # want to increment memo by 1
        memo_item.save()
    except MemoItem.DoesNotExist:
        memo_item = MemoItem.objects.create(
            job = job,# pass in which job should be in the memo
            quantity = 1,
            memo = memo, # we now create the cart 
        )
        memo_item.save() # save the memoitem
   
    return redirect('memo') # redirect the user to the memo page

def memo(request, memo_items=None): 
    try: 
        memo = Memo.objects.get(memo_id=_memo_id(request))
        memo_items = MemoItem.objects.filter(memo=memo, is_active=True)

    except ObjectDoesNotExist: # but if the memo_item does not exst pass
        pass

    context = {
        'memo_items': memo_items,
    }
    return render(request, 'memo.html', context)

# -------------------
# create order 
def place_order(request):
    current_user = request.user
    # if cart count is less or equal to 0 then send back to list of jobs
    memo_items = MemoItem.objects.filter(user=current_user)
    memo_count = memo_items.count()
    if memo_count <= 0:
        return redirect('home') # return to the list of jobs 
    

    if request.method == 'POST':
        form = OrderForm(request.POST) # we need to receive post from the order form
        if form.is_valid():
            # store all the info inside the order table
            data = OrderForm() # instance of order
            data.setter_fname= form.cleaned_data('setter_fname')
            data.setter_lname= form.cleaned_data('setter_lname')
            data.setter_email= form.cleaned_data('setter_email')
            data.note= form.cleaned_data('note')
            
            