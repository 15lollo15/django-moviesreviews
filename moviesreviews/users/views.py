from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from users.models import Comment, Review

@login_required
def like(request):
    review_pk = request.GET['reviewpk']
    user = get_object_or_404(User, username=request.user)
    review = get_object_or_404(Review, pk = review_pk)

    r_text = "like"
    if user.profile in review.likes.all():
        review.likes.remove(user.profile)
        r_text = "not_like"
    else:
        review.likes.add(user.profile)
    r_text += "," + str(len(review.likes.all()))

    return HttpResponse(r_text)
