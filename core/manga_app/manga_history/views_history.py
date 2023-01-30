from ..models import HistoryManga


def manga_history(request, manga, user):

    if HistoryManga.objects.filter(manga=manga, user=user).exists():
       print("Já existe!")
    else:
        history = HistoryManga.objects.create(manga=manga, user=user)
        history.save()

        return history
        

