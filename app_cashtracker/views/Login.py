from app_cashtracker.views.General import *


def login(request):
    # if this user is already logged so redirect to home page
    user_id = request.session.get('user_id', False)
    if user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:home'))

    context = RequestContext(request)
    template = loader.get_template('app_cashtracker/login.html')
    return HttpResponse(template.render(context))


def login_action(request):
    error = False
    email = request.POST['email']
    password = request.POST['password']
    is_mobile = request.POST.get('mobile')

    try:
        user = get_object_or_404(User, email=email)
        if not check_password(user.password, password):
            error = True
        else:
            request.session['user_id'] = user.id
            if request.POST.get('remember_me', False) != 'on':
                request.session.set_expiry(0)  # one week

    except Exception:
        error = True

    # if this user is already logged so redirect to home page
    user_id = request.session.get('user_id', False)
    if user_id:
        if is_mobile is '1':
            return HttpResponse(
                json.dumps(
                    {'user_id': user_id, 'error': error},
                    separators=(',', ':'))
                )
        else:
            return HttpResponseRedirect(reverse('app_cashtracker:home'))

    context_vars = {
        'error': error,
        'user_id': user_id
    }

    context = RequestContext(request, context_vars)
    template = loader.get_template('app_cashtracker/login.html')
    if is_mobile is '1':
        return HttpResponse(json.dumps(context_vars, separators=(',', ':')))
    else:
        return HttpResponse(template.render(context))


def logout(request):
    # if this user is already logged so redirect to home page
    user_id = request.session.get('user_id', False)
    if user_id:
        request.session.clear()

    return HttpResponseRedirect(reverse('app_cashtracker:login'))
