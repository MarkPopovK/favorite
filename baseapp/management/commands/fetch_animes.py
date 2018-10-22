from django.core.management.base import BaseCommand, CommandError
from baseapp.models import Interest
import time, json
import jikanpy

jikan = jikanpy.Jikan()


class Command(BaseCommand):
    help = 'Fetches anime from MAL'

    def handle(self, *args, **options):
        # all_years = jikan.season_archive()['archive']
        SEASONS = ["Winter", "Spring", "Summer", "Fall"]
        YEARS_RANGE = range(1980, 2020)
        # for anime_year in all_years:
        #     print(len(anime_year['seasons']))
        all_anime = {}
        for year in YEARS_RANGE:
            print(f'{year} in {YEARS_RANGE}')
            year_anime = []
            for season in SEASONS:
                while True:
                    try:
                        anime_season = jikan.season(year, season)['anime']
                        break
                    except jikanpy.exceptions.APIException:
                        print('oops too fast')
                        time.sleep(10)
                    except Exception as e:
                        raise e
                    finally:
                        time.sleep(.5)
                for anime in anime_season:
                    anime['title'] += f' ({year})'
                    all_anime[anime['mal_id']] = anime
                #year_anime += anime_season
            #all_anime += year_anime
            print(len(all_anime))
        # print(len(all_anime))
        useful_anime_data = []
        for anime in all_anime.values():
            useful_anime_data.append({
                'name': anime['title'],
                'thumbnail': anime['image_url'],
                'score': anime['score'],
            })
        with open('animes.json', 'w') as output:
            json.dump(useful_anime_data, output)
        print('total animes: ', len(useful_anime_data))
