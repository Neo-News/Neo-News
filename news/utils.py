from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paging(page, lists, num):
    paginator = Paginator(lists, num)
    try:
        lists_obj = paginator.page(page)
    except PageNotAnInteger:
        lists_obj = paginator.page(1)
    except EmptyPage:
        lists_obj = paginator.page(paginator.num_pages)
    #  페이징 번호 5개씩 보이기 로직
    index = lists_obj.number
    max_index = len(paginator.page_range)
    page_size = 5
    current_page = int(index) if index else 1
    start_index = int((current_page - 1) / page_size) * page_size
    end_index = start_index + page_size
    if end_index >= max_index:
        end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
    return page_range, lists_obj