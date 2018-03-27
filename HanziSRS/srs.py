from datetime import timedelta, datetime
import re
import json

from HanziSRS.dir import user_path

with open(user_path("user.json")) as f:
    SRS_INTERVAL = json.load(f)['settings']['srs_interval']
    SRS_TYPES = list(SRS_INTERVAL.keys())


def next_review_date(srs, srs_type):
    return datetime.now() + string_to_timedelta(SRS_INTERVAL[SRS_TYPES[srs_type-1]][srs])


def next_review_timestamp(srs, srs_type):
    return int(next_review_date(srs, srs_type).timestamp())


def correct_next_srs(srs, srs_type):
    if srs < len(SRS_TYPES[srs_type]):
        return srs, srs_type
    else:
        if srs_type < len(SRS_TYPES):
            return 0, srs_type+1
        else:
            return srs-1, srs_type


def string_to_timedelta(time_string: str):
    def findall():
        for match_obj in re.finditer(r'(\d+)(\w+)', time_string):
            num_str, time_type = match_obj.groups()
            num = int(num_str)

            yield {
                'y': timedelta(days=num*365),
                'yr': timedelta(days=num*365),
                'M': timedelta(weeks=num*4),
                'mo': timedelta(weeks=num*4),
                'w': timedelta(weeks=num),
                'wk': timedelta(weeks=num),
                'd': timedelta(days=num),
                'h': timedelta(hours=num),
                'hr': timedelta(hours=num),
                'm': timedelta(minutes=num),
                'min': timedelta(minutes=num),
                's': timedelta(seconds=num),
                'sec': timedelta(seconds=num)
            }.get(time_type, timedelta(hours=num))

    return sum(findall(), timedelta(0))


if __name__ == '__main__':
    print(next_review_date(1, 1))
