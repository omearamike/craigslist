#!/usr/bin/env python3

import logging
import simplejson as json
from craigslist.search import query_jsonsearch
from craigslist.utils import ActionNoYes

if __name__ == '__main__':

    import argparse

    availability_choices = {'all_dates': 0, 'within_30_days': 1, 'beyond_30_days': 2}

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('city')
    parser.add_argument('--postal', help="postal code to center search results around")
    parser.add_argument('--distance', type=int, help="distance in miles from the postal code")
    parser.add_argument('--min_price')
    parser.add_argument('--max_price')
    parser.add_argument('--has_picture', action='store_true', default=None)
    parser.add_argument('--availability', choices=availability_choices)
    parser.add_argument('--verbose', action="store_true")
    parser.add_argument('--detail', action="store_true")
    parser.add_argument('--executor_class')
    # parser._add_action(ActionNoYes('foo', 'foo', help="Do (or do not) foo. (default do)"))

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='[%(name)s | Thread: %(thread)d %(threadName)s | Process: %(process)d %(processName)s] %(asctime)s %(message)s')
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)

    params = {
        "get_detailed_posts": args.detail,
        "postal": args.postal,
        "search_distance": args.distance,
        "min_price": args.min_price,
        "max_price": args.max_price,
        "hasPic": int(args.has_picture) if args.has_picture else None,
        "availabilityMode": availability_choices.get(args.availability)
    }

    if args.executor_class:
        params['executor_class'] = args.executor_class

    for post in query_jsonsearch(args.city, **params):
        print(json.dumps(post, namedtuple_as_object=True))
