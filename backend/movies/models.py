from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL  # 커스텀 User 고려


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Movie(TimeStampedModel):
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    poster_url = models.URLField(max_length=500, blank=True)
    overview = models.TextField(blank=True)

    genres = models.ManyToManyField(
        'Genre',
        through='MovieGenre',
        related_name='movies',
        blank=True,
    )

    persons = models.ManyToManyField(
        'Person',
        through='MovieCast',
        related_name='movies',
        blank=True,
    )

    def __str__(self):
        return self.title

    @property
    def avg_score(self):
        agg = self.ratings.aggregate(avg=models.Avg('score'))
        return agg['avg']

    @property
    def short_review(self):
        """가장 최근 리뷰 기준 한 줄 요약"""
        review = self.reviews.order_by('-created_at').first()
        if not review:
            return None

        text = (review.content or "").strip()
        if len(text) <= 30:
            return text
        return text[:30] + "..."


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Person(TimeStampedModel):
    name = models.CharField(max_length=100)
    profile = models.TextField(blank=True)

    def __str__(self):
        return self.name


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genre_movies')

    class Meta:
        unique_together = ('movie', 'genre')

    def __str__(self):
        return f'{self.movie} - {self.genre}'


class MovieCast(models.Model):
    ROLE_CHOICES = (
        ('actor', '배우'),
        ('director', '감독'),
        ('staff', '스태프'),
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='casts')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='casts')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    character_name = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ('movie', 'person', 'role')

    def __str__(self):
        return f'{self.movie} - {self.person} ({self.role})'


class Rating(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    score = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f'{self.user} - {self.movie} ({self.score})'


class Review(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=50, blank=True)   # 닉네임 (로그인 붙이면 User FK로 바꿔도 됨)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.movie.title} - {self.author}'


class LikeReview(TimeStampedModel):
    # ⚠️ 문자열로 'movies.Review' 를 명시해서 앱 레지스트리 문제 방지
    review = models.ForeignKey('movies.Review', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_reviews')

    class Meta:
        unique_together = ('review', 'user')

    def __str__(self):
        return f'{self.user} likes {self.review_id}'


class WatchList(TimeStampedModel):
    STATUS_CHOICES = (
        ('WANT', '보고싶어요'),
        ('DONE', '봤어요'),
        ('DROP', '중단'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchlist_entries')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WANT')

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f'{self.user} - {self.movie} ({self.status})'
