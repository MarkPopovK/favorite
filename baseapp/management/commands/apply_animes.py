from django.core.management.base import BaseCommand, CommandError
from baseapp.models import Interest
import time, json, requests
import jikanpy
from django.core import files
from io import BytesIO

s = requests.Session()


class Command(BaseCommand):
    help = 'Downloads thumbnails + applies to the DB anime from animes.json created by fetch_anime command'

    def handle(self, *args, **options):
        with open('animes.json', 'r') as _input:
            animes = json.load(_input)

        animes = [anime for anime in animes if anime['score']]
        for i, anime in enumerate(sorted(animes, key=lambda a: a['score'], reverse=True)):
            if Interest.objects.filter(name=anime['name'], interest_type='A').exists():
                print('skip')
                continue

            new_anime = Interest()
            new_anime.name = anime['name']
            new_anime.interest_type = 'A'

            if i <= 1000:
                while True:
                    resp = s.get(anime['thumbnail'])
                    if resp.status_code == requests.codes.ok:
                        time.sleep(.2)
                        break
                    else:
                        print("blya")
                        time.sleep(10)
                fp = BytesIO()
                fp.write(resp.content)
                file_name = anime['name'] + '_thumb.jpg'
                new_anime.thumbnail.save(file_name, files.File(fp))
            else:
                new_anime.save()

            print(new_anime.name)
        print(len(animes))
