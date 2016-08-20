from django.conf import settings
from indexman.models import MappingUrlTimestamp
import redis

shared_folder_path = settings.SHARED_FOLDER_PATH


def read_file(file_path):
    with open(file_path, 'r') as fp:
        first_line = fp.readline()
        # http://www.katespade.com/products/georgica-beach-bralette/S32040.html?dwvar_S32040_size=XS&dwvar_S32040_color=001   1469596658007   200
        url, parsed_ts, status_code = first_line.strip().split('\t')
        url = u'{}'.format(url)
        html_str = fp.read()
        # return url, parsed_ts, status_code, html_str

        save_to_model(file_path, url, parsed_ts, status_code, html_str)


def save_to_model(file_name, url, parsed_ts, status_code, html_str):
    mdl = MappingUrlTimestamp(url=url, filename=file_name, indexed_timestamp=parsed_ts, status_code=status_code)
    mdl.save()
    md5_hash = mdl.md5
    r = redis.StrictRedis()
    r.set('{}__{}'.format(md5_hash, parsed_ts), html_str)
