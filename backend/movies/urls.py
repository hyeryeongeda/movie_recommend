from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    MovieListAPIView, MovieDetailAPIView,
    RatingCreateUpdateAPIView,
    ReviewListCreateAPIView, ReviewLikeToggleAPIView,
    WatchListToggleAPIView, SimilarMovieAPIView, MyWatchListAPIView,
    MovieListAPIView, MovieDetailAPIView, SimilarMovieAPIView,
    RegisterAPIView, MeAPIView
)

urlpatterns = [
    path('movies/', MovieListAPIView.as_view()),
    path('movies/<int:pk>/', MovieDetailAPIView.as_view()),

    # ⭐ 반드시 ratings로!
    path('movies/<int:movie_pk>/ratings/', RatingCreateUpdateAPIView.as_view()),

    path('movies/<int:movie_id>/reviews/', ReviewListCreateAPIView.as_view()),
    path('reviews/<int:review_pk>/like/', ReviewLikeToggleAPIView.as_view()),
    path('movies/<int:movie_pk>/watchlist-toggle/', WatchListToggleAPIView.as_view()),
    path('movies/<int:movie_id>/similar/', SimilarMovieAPIView.as_view()),
    path('watchlist/me/', MyWatchListAPIView.as_view()),

    path('auth/register/', RegisterAPIView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', MeAPIView.as_view()),
]

