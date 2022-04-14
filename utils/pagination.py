from django.core.paginator import Paginator

def make_pagination_range(range_pages = list(range(1,21)),qty_pages = 4,current_page = 1):
    
    middle = qty_pages // 2 
    start = current_page - middle 
    end = current_page + middle  
    total_pages = len(range_pages)

    start_range_offset = abs(start) if start < 0 else 0 

    if start < 0:
        start = 0 
        end += start_range_offset 

    if current_page > (total_pages - middle):
        start = len(range_pages) - qty_pages

    pagination = range_pages[start:end]

    return {
        'range_pages': range_pages,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'start': start,
        'end': end,
        'total_pages': total_pages,
        'pagination': pagination,
        'start_out_of_range': current_page > middle,
        'end_out_of_range': end < total_pages,
    }

def make_pagination(request,queryset,per_page,qty_pages = 4):
    
    try:
        current_page = int(request.GET.get('page')) 
    except TypeError:
        current_page = 1
    
    paginator = Paginator(queryset,per_page)
    obj = paginator.get_page(current_page) 

    pagination_range = make_pagination_range(
        paginator.page_range,
        qty_pages,
        current_page
    )

    return obj,pagination_range