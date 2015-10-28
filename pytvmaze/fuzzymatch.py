#!/usr/bin/python

from __future__ import print_function
from datetime import datetime
import tvmaze

# Check if user has added extra classifiers such as year, country, etc.
def parse_user_text(user_text):
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

def fuzzy_search(qualifiers, results):

    maze_score = sorted([(show['score'],
                         show['show']['id'])
                         for show in results],
                        reverse=True)
    if len(maze_score) > 1 and maze_score[0][0] > maze_score[1][0]:
        return maze_score[0][1]

    else:
        matches = {}
        # If we found qualifiers
        if qualifiers:
            for show in results:
                # matches[show.get('show').get('id')] = 0
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
                    'premiered':premiered}

            # Sort the matches by number of matched qualifiers
            match_score = sorted(matches,
                                 key=lambda k: matches[k]['fuzzy_score'],
                                 reverse=True)

            # In case of tie prefer the show with the most recent premeier date
            if (len(match_score) > 1 and
                matches[match_score[0]]['fuzzy_score'] == \
                matches[match_score[1]]['fuzzy_score']):

                print('\nMultiple shows matched this search,',
                      'try providing more information\nin your search such as',
                      'premier year, country code(us, au, gb, etc.), network,',
                      '\nor language.  Otherwise the show with the most',
                      'recent premier date will be chosen\n')
                if (datetime.strptime(matches[match_score[0]]['premiered'],
                                      '%Y-%m-%d').date() >
                    datetime.strptime(matches[match_score[1]]['premiered'],
                                      '%Y-%m-%d').date()
                   ):
                    return match_score[0]
                else:
                    return match_score[1]

            return max(matches, key=lambda key: matches[key])
        else:
            # If no qualifiers return show with the most recent premier date
            if (len(maze_score) > 1 and
                maze_score[0][0] == maze_score[1][0] and
                not qualifiers):

                print('\nMultiple shows matched this search,',
                      'try providing more information\nin your search such as',
                      'premier year, country code(us, au, gb, etc.), network,',
                      '\nor language.  Otherwise the show with the most',
                      'recent premier date will be chosen\n')

                newest = sorted(results,
                                key=lambda k: k['show']['premiered'],
                                reverse=True)
                return newest[0]['show']['id']

            # If no qualifiers
            return results[0]['show']['id']
