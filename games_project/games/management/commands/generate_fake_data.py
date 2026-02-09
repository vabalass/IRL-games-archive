import random

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from games_project.feedback.models import Comment
from games_project.games.models import Category
from games_project.games.models import Environment
from games_project.games.models import Game
from games_project.users.models import User

fake = Faker()
GAME_CATEGORIES = [
    "Gaudynės",
    "Slėpynės",
    "Žongliravimas",
    "Medžioklė",
    "Žvėjyba",
    "Žygis",
    "Kvadratas",
    "Pasivaikščiojimas",
    "Susipažinimas",
    "Tvarkymasis",
    "Dienos aptarimas",
]


class Command(BaseCommand):
    help = "Generated fake data for the DB."

    def add_arguments(self, parser):
        parser.add_argument(
            "model",
            type=str,
            choices=["all", "games", "categories", "comments", "users"],
            help="Model type for generation",
        )
        parser.add_argument(
            "--count",
            type=int,
            default=5,
            help="Number of object to generate (default = 5).",
        )

    def handle(self, *args, **options):
        model = options["model"]
        count = options["count"]

        if model == "all":
            self._create_all(count)
        elif model == "games":
            self._create_games(count)
        elif model == "categories":
            self._create_categories(count)
        elif model == "comments":
            self._create_comments(count)
        elif model == "users":
            self._create_users(count)

    def _create_all(self, count):
        self._create_users(5)
        self._create_categories(len(GAME_CATEGORIES))
        self._create_games(count)
        self._create_comments(count)

    def _create_games(self, count):
        categories = list(Category.objects.all())
        if not categories:
            self.stdout.write(
                self.style.ERROR(
                    "No categories found, please create categories first.",
                ),
            )
            return

        for i in range(count):
            title = random.choice(GAME_CATEGORIES) + " pagal " + fake.first_name()
            slug = f"{slugify(title)}-{i}"
            Game.objects.create(
                title=title,
                slug=slug,
                description=fake.paragraph(),
                environment=random.choice(Environment.values),
                min_players=random.randint(2, 15),
                max_players=random.randint(20, 100),
                min_duration=random.randint(5, 30),
                max_duration=random.randint(40, 90),
                category=random.choice(categories),
                equipment=fake.sentence(nb_words=1),
            )

        self.stdout.write(self.style.SUCCESS(f"Created {count} games."))

    def _create_categories(self, count):
        created_count = 0

        for _ in range(count):
            title = random.choice(GAME_CATEGORIES)
            slug = slugify(title)

            _, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "description": fake.paragraph(),
                },
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created_count} categories."))

    def _create_comments(self, count):
        games = list(Game.objects.all())
        users = list(User.objects.all())

        if not games:
            self.stdout.write(
                self.style.ERROR(
                    "No games found, please create games first.",
                ),
            )
            return

        if not users:
            self.stdout.write(
                self.style.ERROR(
                    "No users found, please create users first.",
                ),
            )
            return

        for _ in range(count):
            game = random.choice(games)
            Comment.objects.create(
                author=random.choice(users),
                game=game,
                text=fake.paragraph()[:30],
                upvotes=random.randint(0, 5),
                downvotes=random.randint(0, 5),
                rating=random.randint(1, 10),
            )

        self.stdout.write(self.style.SUCCESS(f"Created {count} comments."))

    def _create_users(self, count):
        created_count = 0

        for i in range(count):
            username = f"{fake.user_name()}_{i}"
            _, created = User.objects.get_or_create(
                username=username,
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created_count} users."))
