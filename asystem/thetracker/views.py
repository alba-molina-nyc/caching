from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Memo, MemoItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

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

def memo(request, total=0, quantity=0, memo_items=None): 
    try: 
        memo = Memo.objects.get(memo_id=_memo_id(request))
        memo_items = MemoItem.objects.filter(memo=memo, is_active=True)

        for memo_item in memo_items:
            # get total paying to the setter
            total += (memo_item.job.num_stones * 0.50)
            quantity += memo_item.quantity
    except ObjectDoesNotExist: # but if the memo_item does not exst pass
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'memo_items': memo_items,
    }
    return render(request, 'memo.html', context)





















#     # If the user is authenticated
#     if current_user.is_authenticated:
#         job_variation = []
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]

#                 try:
#                     variation = Variation.objects.get(job=job, variation_category__iexact=key, variation_value__iexact=value)
#                     job_variation.append(variation)
#                 except:
#                     pass


#         is_memo_item_exists = memoItem.objects.filter(job=job, user=current_user).exists()
#         if is_memo_item_exists:
#             memo_item = memoItem.objects.filter(job=job, user=current_user)
#             ex_var_list = []
#             id = []
#             for item in memo_item:
#                 existing_variation = item.variations.all()
#                 ex_var_list.append(list(existing_variation))
#                 id.append(item.id)

#             if job_variation in ex_var_list:
#                 # increase the memo item quantity
#                 index = ex_var_list.index(job_variation)
#                 item_id = id[index]
#                 item = memoItem.objects.get(job=job, id=item_id)
#                 item.quantity += 1
#                 item.save()

#             else:
#                 item = memoItem.objects.create(job=job, quantity=1, user=current_user)
#                 if len(job_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*job_variation)
#                 item.save()
#         else:
#             memo_item = memoItem.objects.create(
#                 job = job,
#                 quantity = 1,
#                 user = current_user,
#             )
#             if len(job_variation) > 0:
#                 memo_item.variations.clear()
#                 memo_item.variations.add(*job_variation)
#             memo_item.save()
#         return redirect('memo')
#     # If the user is not authenticated
#     else:
#         job_variation = []
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]

#                 try:
#                     variation = Variation.objects.get(job=job, variation_category__iexact=key, variation_value__iexact=value)
#                     job_variation.append(variation)
#                 except:
#                     pass


#         try:
#             memo = memo.objects.get(memo_id=_memo_id(request)) # get the memo using the memo_id present in the session
#         except memo.DoesNotExist:
#             memo = memo.objects.create(
#                 memo_id = _memo_id(request)
#             )
#         memo.save()

#         is_memo_item_exists = memoItem.objects.filter(job=job, memo=memo).exists()
#         if is_memo_item_exists:
#             memo_item = memoItem.objects.filter(job=job, memo=memo)
#             # existing_variations -> database
#             # current variation -> job_variation
#             # item_id -> database
#             ex_var_list = []
#             id = []
#             for item in memo_item:
#                 existing_variation = item.variations.all()
#                 ex_var_list.append(list(existing_variation))
#                 id.append(item.id)

#             print(ex_var_list)

#             if job_variation in ex_var_list:
#                 # increase the memo item quantity
#                 index = ex_var_list.index(job_variation)
#                 item_id = id[index]
#                 item = memoItem.objects.get(job=job, id=item_id)
#                 item.quantity += 1
#                 item.save()

#             else:
#                 item = memoItem.objects.create(job=job, quantity=1, memo=memo)
#                 if len(job_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*job_variation)
#                 item.save()
#         else:
#             memo_item = memoItem.objects.create(
#                 job = job,
#                 quantity = 1,
#                 memo = memo,
#             )
#             if len(job_variation) > 0:
#                 memo_item.variations.clear()
#                 memo_item.variations.add(*job_variation)
#             memo_item.save()
#         return redirect('memo')


# def remove_memo(request, job_id, memo_item_id):

#     job = get_object_or_404(Job, id=job_id)
#     try:
#         if request.user.is_authenticated:
#             memo_item = memoItem.objects.get(job=job, user=request.user, id=memo_item_id)
#         else:
#             memo = memo.objects.get(memo_id=_memo_id(request))
#             memo_item = memoItem.objects.get(job=job, memo=memo, id=memo_item_id)
#         if memo_item.quantity > 1:
#             memo_item.quantity -= 1
#             memo_item.save()
#         else:
#             memo_item.delete()
#     except:
#         pass
#     return redirect('memo')


# def remove_memo_item(request, job_id, memo_item_id):
#     job = get_object_or_404(job, id=job_id)
#     if request.user.is_authenticated:
#         memo_item = memoItem.objects.get(job=job, user=request.user, id=memo_item_id)
#     else:
#         memo = memo.objects.get(memo_id=_memo_id(request))
#         memo_item = memoItem.objects.get(job=job, memo=memo, id=memo_item_id)
#     memo_item.delete()
#     return redirect('memo')


# def memo(request, total=0, quantity=0, memo_items=None):
#     try:
#         tax = 0
#         grand_total = 0
#         if request.user.is_authenticated:
#             memo_items = memoItem.objects.filter(user=request.user, is_active=True)
#         else:
#             memo = memo.objects.get(memo_id=_memo_id(request))
#             memo_items = memoItem.objects.filter(memo=memo, is_active=True)
#         for memo_item in memo_items:
#             total += (memo_item.job.price * memo_item.quantity)
#             quantity += memo_item.quantity
#         tax = (2 * total)/100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass #just ignore

#     context = {
#         'total': total,
#         'quantity': quantity,
#         'memo_items': memo_items,
#         'tax'       : tax,
#         'grand_total': grand_total,
#     }
#     return render(request, 'store/memo.html', context)


# @login_required(login_url='login')
# def checkout(request, total=0, quantity=0, memo_items=None):
#     try:
#         tax = 0
#         grand_total = 0
#         if request.user.is_authenticated:
#             memo_items = memoItem.objects.filter(user=request.user, is_active=True)
#         else:
#             memo = memo.objects.get(memo_id=_memo_id(request))
#             memo_items = memoItem.objects.filter(memo=memo, is_active=True)
#         for memo_item in memo_items:
#             total += (memo_item.job.price * memo_item.quantity)
#             quantity += memo_item.quantity
#         tax = (2 * total)/100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass #just ignore

#     context = {
#         'total': total,
#         'quantity': quantity,
#         'memo_items': memo_items,
#         'tax'       : tax,
#         'grand_total': grand_total,
#     }
#     return render(request, 'store/checkout.html', context)
# -----


#     from django.shortcuts import render, redirect, get_object_or_404
# from .models import Job, Memo, MemoItem
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.decorators import login_required

# # Create your views here.
# from django.http import HttpResponse

# # create private function from this request we are going to take the memo.id
# def _memo_id(request):
#     # session_key -> session_id,
#     memo = request.session.session_key
#     if not memo:
#         memo = request.session.create()
#     # return the memo & memo id
#     return memo

# # add job inside the memo, so need job_id
# def add_memo(request, job_id):
#     current_user = request.user
#     job = Job.objects.get(id=job_id) #get the job
#     # If the user is authenticated
#     if current_user.is_authenticated:
#         job_variation = []
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]

#                 try:
#                     variation = Variation.objects.get(job=job, variation_category__iexact=key, variation_value__iexact=value)
#                     job_variation.append(variation)
#                 except:
#                     pass


#         is_memo_item_exists = memoItem.objects.filter(job=job, user=current_user).exists()
#         if is_memo_item_exists:
#             memo_item = memoItem.objects.filter(job=job, user=current_user)
#             ex_var_list = []
#             id = []
#             for item in memo_item:
#                 existing_variation = item.variations.all()
#                 ex_var_list.append(list(existing_variation))
#                 id.append(item.id)

#             if job_variation in ex_var_list:
#                 # increase the memo item quantity
#                 index = ex_var_list.index(job_variation)
#                 item_id = id[index]
#                 item = memoItem.objects.get(job=job, id=item_id)
#                 item.quantity += 1
#                 item.save()

#             else:
#                 item = memoItem.objects.create(job=job, quantity=1, user=current_user)
#                 if len(job_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*job_variation)
#                 item.save()
#         else:
#             memo_item = memoItem.objects.create(
#                 job = job,
#                 quantity = 1,
#                 user = current_user,
#             )
#             if len(job_variation) > 0:
#                 memo_item.variations.clear()
#                 memo_item.variations.add(*job_variation)
#             memo_item.save()
#         return redirect('memo')
#     # If the user is not authenticated
#     else:
#         job_variation = []
#         if request.method == 'POST':
#             for item in request.POST:
#                 key = item
#                 value = request.POST[key]

#                 try:
#                     variation = Variation.objects.get(job=job, variation_category__iexact=key, variation_value__iexact=value)
#                     job_variation.append(variation)
#                 except:
#                     pass


#         try:
#             memo = memo.objects.get(memo_id=_memo_id(request)) # get the memo using the memo_id present in the session
#         except memo.DoesNotExist:
#             memo = memo.objects.create(
#                 memo_id = _memo_id(request)
#             )
#         memo.save()

#         is_memo_item_exists = memoItem.objects.filter(job=job, memo=memo).exists()
#         if is_memo_item_exists:
#             memo_item = memoItem.objects.filter(job=job, memo=memo)
#             # existing_variations -> database
#             # current variation -> job_variation
#             # item_id -> database
#             ex_var_list = []
#             id = []
#             for item in memo_item:
#                 existing_variation = item.variations.all()
#                 ex_var_list.append(list(existing_variation))
#                 id.append(item.id)

#             print(ex_var_list)

#             if job_variation in ex_var_list:
#                 # increase the memo item quantity
#                 index = ex_var_list.index(job_variation)
#                 item_id = id[index]
#                 item = memoItem.objects.get(job=job, id=item_id)
#                 item.quantity += 1
#                 item.save()

#             else:
#                 item = memoItem.objects.create(job=job, quantity=1, memo=memo)
#                 if len(job_variation) > 0:
#                     item.variations.clear()
#                     item.variations.add(*job_variation)
#                 item.save()
#         else:
#             memo_item = memoItem.objects.create(
#                 job = job,
#                 quantity = 1,
#                 memo = memo,
#             )
#             if len(job_variation) > 0:
#                 memo_item.variations.clear()
#                 memo_item.variations.add(*job_variation)
#             memo_item.save()
#         return redirect('memo')


# def remove_memo(request, job_id, memo_item_id):

#     job = get_object_or_404(Job, id=job_id)
#     try:
#         if request.user.is_authenticated:
#             memo_item = memoItem.objects.get(job=job, user=request.user, id=memo_item_id)
#         else:
#             memo = memo.objects.get(memo_id=_memo_id(request))
#             memo_item = memoItem.objects.get(job=job, memo=memo, id=memo_item_id)
#         if memo_item.quantity > 1:
#             memo_item.quantity -= 1
#             memo_item.save()
#         else:
#             memo_item.delete()
#     except:
#         pass
#     return redirect('memo')


# def remove_memo_item(request, job_id, memo_item_id):
#     job = get_object_or_404(job, id=job_id)
#     if request.user.is_authenticated:
#         memo_item = memoItem.objects.get(job=job, user=request.user, id=memo_item_id)
#     else:
#         memo = memo.objects.get(memo_id=_memo_id(request))
#         memo_item = memoItem.objects.get(job=job, memo=memo, id=memo_item_id)
#     memo_item.delete()
#     return redirect('memo')


# def memo(request, total=0, quantity=0, memo_items=None):
#     try:
#         tax = 0
#         grand_total = 0
#         if request.user.is_authenticated:
#             memo_items = memoItem.objects.filter(user=request.user, is_active=True)
#         else:
#             memo = memo.objects.get(memo_id=_memo_id(request))
#             memo_items = memoItem.objects.filter(memo=memo, is_active=True)
#         for memo_item in memo_items:
#             total += (memo_item.job.price * memo_item.quantity)
#             quantity += memo_item.quantity
#         tax = (2 * total)/100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass #just ignore

#     context = {
#         'total': total,
#         'quantity': quantity,
#         'memo_items': memo_items,
#         'tax'       : tax,
#         'grand_total': grand_total,
#     }
#     return render(request, 'store/memo.html', context)


# @login_required(login_url='login')
# def checkout(request, total=0, quantity=0, memo_items=None):
#     try:
#         tax = 0
#         grand_total = 0
#         if request.user.is_authenticated:
#             memo_items = memoItem.objects.filter(user=request.user, is_active=True)
#         else:
#             memo = memo.objects.get(memo_id=_memo_id(request))
#             memo_items = memoItem.objects.filter(memo=memo, is_active=True)
#         for memo_item in memo_items:
#             total += (memo_item.job.price * memo_item.quantity)
#             quantity += memo_item.quantity
#         tax = (2 * total)/100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass #just ignore

#     context = {
#         'total': total,
#         'quantity': quantity,
#         'memo_items': memo_items,
#         'tax'       : tax,
#         'grand_total': grand_total,
#     }
#     return render(request, 'store/checkout.html', context)