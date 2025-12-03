from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import (
    Movie, Genre, Person, MovieGenre, MovieCast,
    Rating, Review, LikeReview, WatchList
)

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'profile')


class MovieCastSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)

    class Meta:
        model = MovieCast
        fields = ('id', 'person', 'role', 'character_name')


class MovieListSerializer(serializers.ModelSerializer):
    avg_score = serializers.FloatField(read_only=True)

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'poster_url',
            'release_year',
            'avg_score',
        )


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    casts = MovieCastSerializer(many=True, read_only=True)
    avg_score = serializers.FloatField(read_only=True)

    # 현재 로그인 유저의 평점/워치리스트 상태
    user_score = serializers.SerializerMethodField()
    is_in_watchlist = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'original_title',
            'overview',
            'poster_url',
            'release_year',
            'country',
            'runtime',
            'genres',
            'casts',
            'avg_score',
            'user_score',
            'is_in_watchlist',
        )

    def get_user_score(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return None
        rating = obj.ratings.filter(user=request.user).first()
        return float(rating.score) if rating else None

    def get_is_in_watchlist(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.watchlist_entries.filter(user=request.user).exists()


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'movie', 'user', 'score', 'created_at', 'updated_at')
        read_only_fields = ('user', 'movie', 'created_at', 'updated_at')


class ReviewSerializer(serializers.ModelSerializer):
    # LikeReview 에서 related_name='likes' 이므로 사용 가능
    like_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'movie',
            'author',
            'content',
            'like_count',
            'created_at',
        )
        read_only_fields = ('movie', 'created_at')

class MovieSerializer(serializers.ModelSerializer):
    # 비슷한 영화 추천용: 간단 카드용 데이터
    avg_score = serializers.FloatField(read_only=True)

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'poster_url',
            'release_year',
            'country',
            'runtime',
            'avg_score',
        )

class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = ('id', 'movie', 'user', 'status', 'created_at')
        read_only_fields = ('user', 'movie', 'created_at')

# ✅ 마이페이지용: 영화 정보까지 같이 주는 시리얼라이저
class WatchListItemSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = WatchList
        fields = ('id', 'movie', 'status', 'created_at')
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user
