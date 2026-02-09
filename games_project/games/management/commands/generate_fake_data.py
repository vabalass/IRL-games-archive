import random

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from games_project.games.models import Category
from games_project.games.models import Environment
from games_project.games.models import Game

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
            choices=["all", "games", "categories"],
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

    def _create_all(self, count):
        self._create_categories(len(GAME_CATEGORIES))
        self._create_games(count)

    def _create_games(self, count):
        categories = Category.objects.all()
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
