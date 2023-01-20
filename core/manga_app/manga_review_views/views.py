from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from manga_app.models import Manga, ReviewManga
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
    else:
        score = HORRIBLE

    return score


def manga_review(request):
    status = ""
    manga_id = request.GET.get('manga_id')
    review = request.GET.get('text')

    if ReviewManga.objects.filter(manga=manga_id, user=request.user).exists():
        review_manga = get_object_or_404(ReviewManga, manga=manga_id, user=request.user)
        score = score_manga(review)
        review_manga.review = score
        review_manga.save()
        status = "Atualizado!"

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

    
