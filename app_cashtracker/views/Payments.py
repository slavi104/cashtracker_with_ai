from app_cashtracker.views.General import *


def home(request):

    user_id = request.session.get('user_id', False)
    subcategories = {}
    is_mobile = request.POST.get('mobile')
    if is_mobile:
        user_id = request.POST.get('user_id')
    print(request.POST)
    if not user_id:
        if is_mobile == '1':
            return HttpResponse(
                json.dumps(
                    {
                        'error': 'Ti si tup!!!',
                    },
                    separators=(',', ':'))
                )
        else:
            return HttpResponseRedirect(reverse('app_cashtracker:login'))

    categories = Category.objects.filter(user_id=user_id, is_active=1)
    if categories.count() == 0:
        categories = Category.objects.filter(user_id=1, is_active=1)

    for category in categories:
        subcategories[category.id] = {}
        category_subcategories = Subcategory.objects.filter(
            category_id=category.id,
            is_active=1
        )
        for subcategory in category_subcategories:
            subcategories[category.id][subcategory.id] = subcategory.name

    user = get_object_or_404(User, id=user_id)
    context = RequestContext(request, {
        'logged_user': user,
        'categories': categories,
        'subcategories': json.dumps(subcategories),
        'date_time': (timezone.now() + timedelta(hours=3)).strftime(
            '%Y-%m-%d %H:%M:%S'
        ),
        'currency': user.currency
    })

    if is_mobile == '1':
        Category.process(user_id)
        return HttpResponse(
            json.dumps(
                {
                    'user_id': user_id,
                    'categories': Category.DEFAULT_CATEGORIES,
                    'currency': user.currency
                },
                separators=(',', ':'))
            )

    template = loader.get_template('app_cashtracker/home.html')
    return HttpResponse(template.render(context))


def add_payment(request):

    print(request.POST)
    user_id = request.session.get('user_id', False)
    is_mobile = request.POST.get('mobile')
    if is_mobile == '1':
        user_id = request.POST.get('user_id')

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    params = request.POST
    payment = Payment()
    payment.value = params['value']
    payment.currency = params['currency']
    payment.category = get_object_or_404(Category, id=params['category'])
    if params.get('subcategory'):
        payment.subcategory = get_object_or_404(
            Subcategory, id=params['subcategory']
        )
    else:
        subcategories = Subcategory.objects.filter(
            category_id=payment.category.id,
            is_active=1
        )
        payment.subcategory = subcategories.first()

    payment.date_time = params['date_time']
    if is_mobile != '1':
        payment.name = params['name']
        payment.comment = params['comment']
    payment.user = get_object_or_404(User, id=user_id)
    payment.is_active = True

    # payment.save()
    try:
        payment.save()
        success = 1
    except Exception:
        success = 0

    if is_mobile == '1':
        return HttpResponse(
            json.dumps(
                {
                    'success': success
                },
                separators=(',', ':'))
            )

    return HttpResponseRedirect(reverse('app_cashtracker:home'))


def payments(request):

    user_id = request.session.get('user_id', False)
    params = request.POST

    is_mobile = request.POST.get('mobile')
    if is_mobile == '1':
        user_id = request.POST.get('user_id')

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    if is_mobile == '1':
        payments = Payment.objects.filter(
                user_id=user_id,
                is_active=1
            )
        result = {}
        for payment in payments:
            result[payment.id] = {
                'Category': payment.category.name,
                'Value': str(payment.value),
                'Date': payment.date_time.strftime('%Y-%m-%d %H@%M@%S')
            }

        return HttpResponse(
            json.dumps(
                result,
                separators=(',', ':'))
            )

    categories = Category.objects.filter(user_id=user_id, is_active=1)
    logged_user = get_object_or_404(User, id=user_id)
    payments_for = params.get('payments_for', 'today')
    payments_curr = params.get('currency', logged_user.currency)
    payments_cat = params.get('category', 0)

    payments = Payment.fetch_payments(
        payments_for,
        payments_cat,
        payments_curr,
        logged_user
    )

    # parse date of payment to be in hours or only date in some cases
    list(map(lambda p: p.parse_date(payments_for), payments))

    # convert all values to choosen currency
    list(map(lambda p: p.convert_currency(payments_curr), payments))

    now = timezone.now()  # + timedelta(hours=3)
    context = RequestContext(request, {
        'logged_user': logged_user,
        'date_time': now.strftime('%Y-%m-%d %H:%M:%S'),
        'payments': payments,
        'payments_for': payments_for,
        'categories': categories,
        'payments_cat': payments_cat,
        'payments_curr': payments_curr
    })

    template = loader.get_template('app_cashtracker/payments.html')
    return HttpResponse(template.render(context))


def delete_payment(request):

    user_id = request.session.get('user_id', False)

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    params = request.POST
    result = {}
    try:
        if int(params['payment_id']) > 0:
            payment = get_object_or_404(Payment, id=int(params['payment_id']))
            payment.is_active = 0
            payment.save()
            result['success'] = 1
    except Exception:
        result['success'] = 0
        result['message'] = 'Error in delete payment'

    return HttpResponse(json.dumps(result, separators=(',', ':')))


def generate_fake_payments(request, number_of_payments=100):
    user_id = request.session.get('user_id', False)

    if not user_id:
        return HttpResponseRedirect(reverse('app_cashtracker:login'))

    # WARNING THIS FUNCTION GENERATE FAKE PAYMENTS
    Payment.generate_fake_payments(
        get_object_or_404(User, id=user_id),
        int(number_of_payments)
    )

    return HttpResponseRedirect(reverse('app_cashtracker:home'))
