from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UpdateUserForm
from django.http import HttpRequest
from eshop.models import Brand, Category

categories = Category.objects.all()
brands = Brand.objects.all()

context = {
    'categories': categories,
    'brands': brands,
}


def register(request: HttpRequest):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account {username} created!')
            return redirect('login')
        else:
            form = UserRegisterForm()
            context.update({'form': form})
            return render(request=request, template_name='registration/registration.html', context=context)
    else:
        form = UserRegisterForm()
        context.update({'form': form})
        return render(request=request, template_name='registration/registration.html', context=context)


@login_required
def profile(request: HttpRequest):
    context.update({
        'orders': request.user.order_set.all().order_by('-pk')
    })
    return render(request, template_name='registration/profile.html', context=context)


@login_required
def update_profile(request: HttpRequest):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your profile is updated successfully!')
            return redirect(to='profile')
    else:
        form = UpdateUserForm(instance=request.user)

    context.update({'form': form})

    return render(request=request, template_name='registration/update_profile.html', context=context)
