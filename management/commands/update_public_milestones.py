from django.core.management.base import BaseCommand, CommandError
from Destiny_Public_Data.utils import UpdatePublicData


class Command(BaseCommand):
    def handle(*args, **options):
        upd = UpdatePublicData()
        upd.blank_databases()
        upd.update_public_milestones()

    help = "Blanks then updates the public milestones databases, call this command from a cron job"

    def add_arguments(self, parser):
        # parser.add_argument('poll_id', nargs='+', type=int)
        pass

