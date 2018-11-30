import sys
import re

from django.core.management.base import BaseCommand
from tqdm import tqdm

from agir.lib.mailtrain import update_person
from ...models import Person, PersonTag


class Command(BaseCommand):
    help = "Tag all emails found in standard input"
    EMAIL_RE = "[a-zA-Z0-9_.+-]+@[a-zA-Z_-]+(?:\.[a-zA-Z_-]+)+"

    def add_arguments(self, parser):
        parser.add_argument("tag")

        parser.add_argument(
            "-c",
            "--create-missing",
            action="store_true",
            dest="create",
            default=False,
            help=(
                "In case emails without a corresponding account are found in input, create "
                "a corresponding account and add it with the tag. By default those accounts are non"
                "members account. WARNING: make sure you have the full consent of all concerned individuals."
            ),
        )
        parser.add_argument(
            "-i",
            "--insoumis",
            action="store_true",
            dest="insoumis",
            default=False,
            help=("Make new accounts full members."),
        )
        parser.add_argument(
            "--tmp",
            action="store_true",
            dest="tmp",
            default=False,
            help=(
                "Does not write the tag in api. If mailtrain is off and create missing is off, the command does nothing."
            ),
        )
        parser.add_argument(
            "-m",
            "--mailtrain",
            action="store_true",
            dest="mailtrain",
            default=False,
            help=("Copy the tag in mailtrain"),
        )

    def handle(self, *args, tag, create, insoumis, tmp, mailtrain, **options):
        emails = re.findall(self.EMAIL_RE, sys.stdin.read())

        persons = []

        for e in emails:
            try:
                persons.append(Person.objects.get_by_natural_key(e))
            except Person.DoesNotExist:
                if create:
                    persons.append(
                        Person.objects.create_person(email=e, is_insoumise=insoumis)
                    )
                    self.stdout.write('Created person "{}"'.format(e))
                else:
                    self.stdout.write('Missing person "{}"'.format(e))

        if persons:
            if tmp is False:
                tag_object, created = PersonTag.objects.get_or_create(label=tag)

                if created:
                    self.stdout.write('Created tag "{}"'.format(tag))

                tag_object.people.add(*persons)

            if mailtrain is True:
                for p in tqdm(persons):
                    update_person(p, tmp_tags=[tag])
