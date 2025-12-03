import requests
from django.core.management.base import BaseCommand
from django.conf import settings

from movies.models import Movie, Genre, Person, MovieCast

TMDB_API_KEY = settings.TMDB_API_KEY
TMDB_IMAGE_BASE = getattr(settings, "TMDB_IMAGE_BASE", "https://image.tmdb.org/t/p/w500")


class Command(BaseCommand):
    help = "TMDB에서 인기 영화 가져와서 Movie/Genre/Person/MovieCast 테이블 채우기"

    def add_arguments(self, parser):
        parser.add_argument(
            "--pages",
            type=int,
            default=1,
            help="가져올 TMDB 인기 영화 페이지 수 (기본 1페이지)",
        )

    def handle(self, *args, **options):
        pages = options["pages"]
        self.stdout.write(self.style.SUCCESS(f"TMDB에서 인기 영화 {pages}페이지 가져오기 시작"))

        for page in range(1, pages + 1):
            self.import_popular_page(page)

        self.stdout.write(self.style.SUCCESS("완료!"))

    # ──────────────────────────────────────
    # 한 페이지(20편) 가져오기
    # ──────────────────────────────────────
    def import_popular_page(self, page: int):
        url = "https://api.themoviedb.org/3/movie/popular"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "ko-KR",
            "page": page,
        }

        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()

        for result in data.get("results", []):
            tmdb_id = result["id"]
            self.import_movie_detail(tmdb_id)

    # ──────────────────────────────────────
    # 영화 상세 + 크레딧까지 가져와서 DB에 저장
    # ──────────────────────────────────────
    def import_movie_detail(self, tmdb_id: int):
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "ko-KR",
            "append_to_response": "credits",
        }

        res = requests.get(url, params=params)
        if res.status_code != 200:
            self.stdout.write(self.style.WARNING(f"영화 {tmdb_id} 불러오기 실패: {res.status_code}"))
            return

        data = res.json()

        title = data.get("title") or data.get("original_title")
        original_title = data.get("original_title") or title
        overview = data.get("overview") or ""
        runtime = data.get("runtime")
        release_date = data.get("release_date")  # '2016-12-25'
        release_year = int(release_date.split("-")[0]) if release_date else None

        # country: 첫 번째 production_countries 기준
        countries = data.get("production_countries") or []
        country = countries[0]["iso_3166_1"] if countries else ""

        poster_path = data.get("poster_path")
        poster_url = TMDB_IMAGE_BASE + poster_path if poster_path else ""

        # Movie 생성/갱신
        movie, created = Movie.objects.update_or_create(
            title=title,
            release_year=release_year,
            defaults={
                "original_title": original_title,
                "overview": overview,
                "runtime": runtime,
                "country": country,
                "poster_url": poster_url,
            },
        )

        msg = "생성" if created else "업데이트"
        self.stdout.write(f"{msg}: {movie.title} ({release_year})")

        # 장르 처리
        self.attach_genres(movie, data.get("genres") or [])

        # 크레딧(감독/배우) 처리
        credits = data.get("credits") or {}
        self.attach_credits(movie, credits)

    # ──────────────────────────────────────
    # 장르 연결 (MovieGenre through 이용)
    # ──────────────────────────────────────
    def attach_genres(self, movie: Movie, genres_data):
        # ManyToMany through라서 바로 movie.genres.set([...]) 는 안 쓰고,
        # Genre만 생성 → movie.genres.add(...) 로 연결
        genre_objs = []
        for g in genres_data:
            name = g.get("name")
            if not name:
                continue
            genre_obj, _ = Genre.objects.get_or_create(name=name)
            genre_objs.append(genre_obj)

        # 기존 장르 교체
        movie.genres.set(genre_objs)

    # ──────────────────────────────────────
    # 크레딧에서 감독 + 배우 상위 몇 명만 저장
    # ──────────────────────────────────────
    def attach_credits(self, movie: Movie, credits_data):
        # 기존 캐스트 제거 후 다시 채우기 (중복 방지)
        movie.casts.all().delete()

        cast_list = credits_data.get("cast") or []
        crew_list = credits_data.get("crew") or []

        # 감독: crew에서 job == 'Director'
        for crew in crew_list:
            if crew.get("job") != "Director":
                continue
            name = crew.get("name")
            if not name:
                continue
            person, _ = Person.objects.get_or_create(name=name)
            MovieCast.objects.get_or_create(
                movie=movie,
                person=person,
                role="director",
                defaults={"character_name": ""},
            )

        # 배우: 상위 5명만
        for cast in cast_list[:5]:
            name = cast.get("name")
            character = cast.get("character") or ""
            if not name:
                continue

            person, _ = Person.objects.get_or_create(name=name)
            MovieCast.objects.get_or_create(
                movie=movie,
                person=person,
                role="actor",
                defaults={"character_name": character},
            )
