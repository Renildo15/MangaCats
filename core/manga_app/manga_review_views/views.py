from django.shortcuts import get_object_or_404
from manga_app.models import Manga, ReviewManga
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
# Constantes com os valores das notas
MASTERPIECE = 5
GOOD = 4
AVERAGE = 3
BAD = 2
HORRIBLE = 1

def score_manga(review):
    score = None

    if review == "Masterpiece":
        score = MASTERPIECE

    elif review == "Good":
        score = GOOD
    
    elif review == "Average":
        score = AVERAGE
       
    elif review == "Bad":
        score = BAD
    elif review == "Horrible":
        score = HORRIBLE
    

    return score

def remove_review(request, manga_id):
    manga_review = get_object_or_404(ReviewManga, manga=manga_id, user=request.user)
    manga_review.delete()
    return True

@login_required(login_url='user:login')
@permission_required("manga_app.add_reviewmanga", login_url='user:login')
def manga_review(request):
    status = ""
    manga_id = request.GET.get('manga_id')
    review = request.GET.get('text')

    

    if ReviewManga.objects.filter(manga=manga_id, user=request.user).exists():
        if review == "Select":
            remove_review(request,manga_id)
            status = 'review deleted'
        review_manga = get_object_or_404(ReviewManga, manga=manga_id, user=request.user)
        score = score_manga(review)
        review_manga.review = score
        review_manga.save()
        status = "changed"

    else:
        manga = get_object_or_404(Manga, id_manga=manga_id)
        score = score_manga(review)
        review_manga = ReviewManga(review=score, manga=manga, user=request.user)
        review_manga.save()
        status = "review"

    data = {'status':status, 'text':review}
    return JsonResponse(data) 


def review_avarege(pk):
    manga = ReviewManga.objects.filter(manga=pk).values_list('review', flat=True)
    try:
        total_reviews = len(manga)
        sum_review = sum(manga)
        manga_len = len(manga)
        average = sum_review/manga_len

        dict = {
            "total_reviews":total_reviews,
            "average": round(average, 2)
        }

        return dict
    except:
        total_reviews = None
        average = None
    dict = {
        "total_reviews":total_reviews,
        "average": average
    }
    return dict


def review_selected(request,pk):
    manga = get_object_or_404(Manga, id_manga=pk)
    review_manga = get_object_or_404(ReviewManga, manga=manga, user=request.user)
    print(review_manga)
    return review_manga

    
