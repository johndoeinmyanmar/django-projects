from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, ItemShareForm 
from .models import Profile, Item 
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from simple_search import search_filter


# Create your views here.

@login_required
def dashboard(request):
	profile = Profile.objects.get(user=request.user)
	item_list = Item.objects.filter(owner=request.user)
	
	return render(request, 'account/dashboard.html', {'profile':profile,'section':'dashboard','item_list':item_list})

@login_required
def post_item(request):
	if request.method == "POST":
		# Post goes here
		if request.is_ajax():
			itemform = ItemShareForm(data=request.POST, files=request.FILES)
			if itemform.is_valid():
				itemform.owner = request.user
				itemform.save()
	return render(request, 'account/dashboard.html', {'section':'dashboard'})
	


def register(request):

	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			# for better safety for password and encryption
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			profile = Profile.objects.create(user = new_user)

			return render(request, 'account/register_done.html',{'new_user':new_user} )

	else:
		user_form = UserRegistrationForm()
	return render(request, 'account/register.html', {'user_form':user_form})

@login_required
def edit(request):

	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user,data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile,
			data=request.POST, files=request.FILES)

		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Profile updated successfully...')
			return redirect('/account/dashboard/')
		else:
			messages.error(request, 'Error Updating your profile...')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)

	return render(request, 'account/edit.html', {'user_form':user_form,'profile_form':profile_form})


@login_required
def shareform(request):

	if request.method == 'POST':
		itemform = ItemShareForm(data=request.POST, files=request.FILES)
		if itemform.is_valid():
			new_item = itemform.save(commit=False)
			new_item.owner = request.user 
			new_item.save()
			messages.success(request, 'Your item has been shared successfully...')
			return redirect('/account/dashboard/')

		else:
			messages.error(request, 'Error uploading your share item...')

	else:
		itemform = ItemShareForm()

	return render(request, 'account/share.html', {'itemform':itemform})


def item_list(request):
	if request.method == 'POST':
		query = request.POST.get('search','')
		search_fields = ['title', 'description', '=item', '=status']
		f = search_filter(search_fields, query)
		object_list = Item.objects.filter(f)
	else:
		object_list = Item.objects.all()
		query = False
	paginator = Paginator(object_list, 8)
	page = request.GET.get('page')
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)

	return render(request, 'account/homepage.html', {'items':items,'page':page,'search':query})

@login_required
def item_edit(request,slug,postfix):
	if slug and postfix == 'delete':
		item = get_object_or_404(Item, slug=slug)
		item.delete()
		profile = Profile.objects.get(user=request.user)
		item_list = Item.objects.filter(owner=request.user)
	
		return render(request, 'account/dashboard.html', {'profile':profile,'section':'dashboard','item_list':item_list})

	elif slug and postfix == 'edit':
		instance = get_object_or_404(Item,slug=slug)
		if request.method == 'POST':
			edit_form = ItemShareForm(data=request.POST,files=request.FILES,instance=instance)
			if edit_form.is_valid():
				update_item = edit_form.save(commit=False)
				update_item.owner = request.user
				update_item.save()
				messages.success(request,'Your item has been updated successfully')
				return redirect('/account/dashboard')
			else:
				messages.error(request,'Error updating your item...')
		else:
			edit_form = ItemShareForm(instance=instance)
	return render(request, 'account/share.html',{'itemform':edit_form,'edit':True})


def show_info(request):
	if request.method == 'GET':
		owner_id = request.GET['owner_id']
		item = Profile.objects.get(user=owner_id)
		response = {}
		response['phone'] = item.phone
		response['location'] = item.location
	
		return JsonResponse(response)