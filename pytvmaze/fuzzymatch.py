#!/usr/bin/python

from __future__ import print_function
from datetime import datetime

WARN_MULTIPLE_RESULTS = ('\nMultiple shows matched this search, '
                'try providing more information\nin your search such as '
                'premier year, country code(us, au, gb, etc.), network, '
                '\nor language. Otherwise the show with the most '
                'recent premier date will be chosen\n')

# Check if user has added extra classifiers such as year, country, etc.
def parse_user_text(user_text):
    # Import locally to avoid circular import
    from pytvmaze import tvmaze
    # Check if there is more than one word
    if ' ' in user_text.strip():
        words = user_text.strip().split(' ')
        qualifiers = []
        # Pop last word until we get results from tvmaze
        for i in range(len(words)):
            s = tvmaze.show_search(' '.join(words))
            if s:
                break
            else:
                print('Performing fuzzy search...')
                # Store popped words
                qualifiers.insert(0, words.pop().lower())
        # Return showname and list of qualifiers
        return {'showname':' '.join(words), 'qualifiers':qualifiers}
    else:
        # If there is only one word, return the text unchanged
        return {'showname':user_text, 'qualifiers':None}

def fuzzy_search(search_text, results):

    showname = search_text['showname'].lower()
    qualifiers = search_text['qualifiers']

    # List sorted by tvmaze score
    maze_score = sorted(
                        [
                            (show['score'], show['show']['id'])
                            for show in results
                        ],
                        reverse=True)

    # If there is only one result with a matching showname, return it
    if (len(maze_score) > 1 and
        maze_score[0][0] > maze_score[1][0] and
        results[0]['show']['name'] != results[1]['show']['name']
    ):
        return maze_score[0][1]

    else:
        matches = {}

        # List of only results with same name as search_text
        filtered_results = [
            show for show in results
            if show['show']['name'].lower() == showname
        ]

        # If we found qualifiers
        if qualifiers and len(filtered_results) > 0:
            for show in filtered_results:
                try:
                    premiered = show['show']['premiered'].lower()
                except:
                    year = ''
                try:
                    country = show['show']['network']['country']['code'].lower()
                except:
                    country = ''
                try:
                    network = show['show']['network']['name'].lower()
                except:
                    network = ''
                try:
                    language = show['show']['language'].lower()
                except:
                    language = ''
                attributes = [premiered[0:4], country, network, language]

                # Store the number of matched qualifiers in the matches dict
                matches[show['show']['id']] = {
                    'fuzzy_score':len(list(set(qualifiers) & set(attributes))),
                    'premiered':premiered
                }

            # Sort the matches by number of matched qualifiers
            match_score = sorted(matches,
                                 key=lambda k: matches[k]['fuzzy_score'],
                                 reverse=True)

            # In case of tie prefer the show with the most recent premeier date
            if (len(match_score) > 1 and
                matches[match_score[0]]['fuzzy_score'] == \
                matches[match_score[1]]['fuzzy_score']
            ):

                print(WARN_MULTIPLE_RESULTS)

                # Choose most recent show
                if (datetime.strptime(matches[match_score[0]]['premiered'],
                                      '%Y-%m-%d').date() > # greater than
                    datetime.strptime(matches[match_score[1]]['premiered'],
                                      '%Y-%m-%d').date()
                ):
                    return match_score[0]
                else:
                    return match_score[1]
            else:
                # Return show with most matched qualifiers
                return max(matches, key=lambda key: matches[key])
        else:
            if len(filtered_results) > 1:

                print(WARN_MULTIPLE_RESULTS)

                # Sort results by premier date
                newest = sorted(filtered_results,
                                key=lambda k: k['show']['premiered'],
                                reverse=True)

                # Return show with latest premier date and matching showname
                return newest[0]['show']['id']
            elif len(filtered_results) == 1:
                # Return only result with matching name
                return filtered_results[0]['show']['id']
            else:
                # If no matching showname, return show with latest premier date
                return results[0]['show']['id']
