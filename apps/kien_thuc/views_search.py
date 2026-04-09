from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from apps.kien_thuc.models import BaiViet, FlashcardSet
from apps.de_thi.models import DeThi

def api_search_suggestions(request):
    """API for real-time search suggestions."""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'results': []})
    
    results = []
    
    # 1. Search Published Articles
    articles = BaiViet.objects.filter(
        Q(tieu_de__icontains=query) | Q(noi_dung__icontains=query),
        status='published'
    )[:5]
    for a in articles:
        results.append({
            'type': 'BaiViet',
            'type_label': '✍️ Bài viết',
            'title': a.tieu_de,
            'url': f'/kien-thuc/bai/{a.id}/',
            'mon': a.mon.ten
        })
        
    # 2. Search Published Flashcard Sets (so_luong_the > 0)
    flashcards = FlashcardSet.objects.filter(
        Q(tieu_de__icontains=query) | Q(mo_ta__icontains=query),
        status='published',
        so_luong_the__gt=0
    )[:5]
    for f in flashcards:
        results.append({
            'type': 'FlashcardSet',
            'type_label': '💡 Flashcard',
            'title': f.tieu_de,
            'url': f'/kien-thuc/flashcard/{f.id}/hoc/',
            'mon': f.mon.ten
        })
        
    # 3. Search Active Exams
    exams = DeThi.objects.filter(
        Q(ten__icontains=query) | Q(mo_ta__icontains=query),
        an=False
    )[:5]
    for e in exams:
        results.append({
            'type': 'DeThi',
            'type_label': '⏱️ Đề thi',
            'title': e.ten,
            'url': f'/de-thi/{e.id}/chon-che-do/',
            'mon': e.mon.ten if e.mon else 'Tổng hợp'
        })
        
    return JsonResponse({'results': results})

def global_search_results(request):
    """Full search results page."""
    query = request.GET.get('q', '').strip()
    
    articles = BaiViet.objects.filter(
        Q(tieu_de__icontains=query) | Q(noi_dung__icontains=query),
        status='published'
    )
    
    flashcards = FlashcardSet.objects.filter(
        Q(tieu_de__icontains=query) | Q(mo_ta__icontains=query),
        status='published',
        so_luong_the__gt=0
    )
    
    exams = DeThi.objects.filter(
        Q(ten__icontains=query) | Q(mo_ta__icontains=query),
        an=False
    )
    
    context = {
        'query': query,
        'articles': articles,
        'flashcards': flashcards,
        'exams': exams,
        'total_results': articles.count() + flashcards.count() + exams.count()
    }
    return render(request, 'search/results.html', context)
