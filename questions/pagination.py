from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def pagination(request, data, count, page):
    global paginator_datas_list
    paginator = Paginator(data, count)
    get = request.GET.get('page')
    if get:
        page = int(get)
    try:
        paginator_datas_list = paginator.page(int(page))
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        paginator_datas_list = paginator.page(paginator.num_pages)
    return paginator_datas_list



