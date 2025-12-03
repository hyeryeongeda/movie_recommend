# movies/views.py
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, Rating, Review, WatchList, LikeReview
from .serializers import (
    MovieListSerializer, MovieDetailSerializer,
    RatingSerializer, ReviewSerializer, WatchListSerializer,
    MovieSerializer, UserSerializer, UserRegisterSerializer, WatchListItemSerializer,
)

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


User = get_user_model()
def get_dummy_user():
    # 임시용: DB에 존재하는 첫 번째 유저를 사용
    # (admin 계정 하나는 꼭 있어야 함!)
    return User.objects.first()


# ─────────────────────────────────────────────
# 영화 목록 / 상세
# ─────────────────────────────────────────────

class MovieListAPIView(generics.ListAPIView):
    queryset = Movie.objects.all().order_by('-id')
    serializer_class = MovieListSerializer


class MovieDetailAPIView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer

    # request 넣어주려고 override
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# ─────────────────────────────────────────────
# 평점 생성/수정
# ─────────────────────────────────────────────

@method_decorator(csrf_exempt, name='dispatch')
class RatingCreateUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, movie_pk):
        movie = get_object_or_404(Movie, pk=movie_pk)
        score = request.data.get('score')

        rating, created = Rating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={'score': score},
        )
        serializer = RatingSerializer(rating)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )



# ─────────────────────────────────────────────
# 리뷰 목록 / 생성 (익명 닉네임 + 내용)
# ─────────────────────────────────────────────

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /api/v1/movies/<movie_id>/reviews/
    POST /api/v1/movies/<movie_id>/reviews/
      body: { "author": "닉네임", "content": "내용" }
    """
    serializer_class = ReviewSerializer
    # ✅ 로그인 안 해도 작성 가능하게 풀기 (임시)
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Review.objects.filter(movie_id=movie_id).order_by('-created_at')

    def perform_create(self, serializer):
        movie_id = self.kwargs['movie_id']
        # Review 모델에 user 필드 없으니까 movie 만 저장
        serializer.save(movie_id=movie_id)



# ─────────────────────────────────────────────
# 리뷰 좋아요 토글
# ─────────────────────────────────────────────

class ReviewLikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, review_pk):
        review = get_object_or_404(Review, pk=review_pk)
        like, created = LikeReview.objects.get_or_create(
            review=review,
            user=request.user,
        )
        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return Response({
            'liked': liked,
            'like_count': review.likes.count(),
        })


# ─────────────────────────────────────────────
# 보고싶어요 / 봤어요 토글
# ─────────────────────────────────────────────

class WatchListToggleAPIView(APIView):
    # ✅ 로그인 없어도 되게 임시 허용
    permission_classes = [permissions.AllowAny]

    def post(self, request, movie_pk):
        """
        status를 body로 받고, 없으면 WANT 기본값
        """
        movie = get_object_or_404(Movie, pk=movie_pk)
        status_value = request.data.get('status', 'WANT')

        # ✅ 로그인 안 되어 있으면 dummy 유저 사용
        if request.user.is_authenticated:
            user = request.user
        else:
            user = get_dummy_user()

        if user is None:
            return Response(
                {'detail': '임시 유저가 없습니다. admin 계정 하나만 먼저 만들어 주세요.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        watch, created = WatchList.objects.update_or_create(
            user=user,
            movie=movie,
            defaults={'status': status_value},
        )
        serializer = WatchListSerializer(watch)
        return Response(serializer.data)



# ─────────────────────────────────────────────
# 비슷한 영화 (나라 기준 간단 추천)
# ─────────────────────────────────────────────

class SimilarMovieAPIView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        movie = Movie.objects.get(id=movie_id)

        # 1) 장르 기준
        qs = Movie.objects.filter(
            genres__in=movie.genres.all()
        ).exclude(id=movie.id).distinct()

        # 2) 없으면 같은 country
        if not qs.exists():
            qs = Movie.objects.filter(
                country=movie.country
            ).exclude(id=movie.id)

        # 3) 그것도 없으면 그냥 인기순 몇 개
        if not qs.exists():
            qs = Movie.objects.exclude(id=movie.id)

        return qs[:10]



# ─────────────────────────────────────────────
# 회원가입 / 내 정보
# ─────────────────────────────────────────────

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class MyWatchListAPIView(generics.ListAPIView):
    """
    GET /api/v1/watchlist/me/
    임시: 로그인 안 되어 있으면 dummy 유저 기준으로 조회
    """
    serializer_class = WatchListItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = get_dummy_user()

        if user is None:
            return WatchList.objects.none()

        return WatchList.objects.filter(
            user=user
        ).select_related('movie').order_by('-created_at')

