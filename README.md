To install:
`pip install pytvmaze`
or download the pytvmaze.py file and place it in your site-packages folder.

Basic single-show usage

```python
import pytvmaze

# Get show object
show = pytvmaze.get_show('dexter')
print show
>>> <pytvmaze.Show instance at 0x107abefc8>
print show.name, show.status, show.maze_id
>>> Dexter Ended 161

# Iterate over episodes
for episode in show.episodes:
  print episode.title
>>> Dexter
>>> Crocodile
>>> Popping Cherry
>>> etc...

# Get a specific episode with: get_episode(season, episode)
ep = show.get_episode(1,8)
print ep
>>> <pytvmaze.Episode instance at 0x107b060e0>
print ep.title
>>> Shrink Wrap

```

There are many possible attributes of the Show class, but since TV Maze is full of user contributions and always being updated, shows will have different available attributes.  Possible attributes are:
```
show.status
show.rating
show.genres
show.weight
show.updated
show.name
show.language
show.schedule
show.url
show.image
show.externals # dict of tvdb and tvrage id's if available
show.premiered
show.summary
show._links # dict of previousepisode and nextepisode keys for their links
show.webChannel
show.runtime
show.type
show.id
show.maze_id # same as show.id
show.network # dict of network properties
show.episodes # list of Episode objects

## Episode object attributes ##
episode.title
episode.airdate
episode.url
episode.season_number
episode.episode_number
episode.image
episode.airstamp
episode.runtime
episode.maze_id
```


Aside from these classes, you can also utilize all of the TV Maze endpoints directly, without creating an insance of the Show class, via their respective functions.  The results of these functions are JSON:

```python
show_search(show) # returns a list of fuzzy-matched shows given a show name (string)
show_single_search(show) # returns the best-matched show
show_single_search(show, embed=[option]) # see http://www.tvmaze.com/api#embedding for embedding other information in your results
lookup_tvrage(tvrage_id) # get tvmaze show data from a tvrage show id
lookup_tvdb(tvdb_id) # get tvmaze show data from a tvdb show id
get_schedule(country='US')
get_full_schedule() # ALL future known episodes.  Several MB large, cached for 24 hours
show_main_info(maze_id)
episode_list(maze_id)
show_cast(maze_id)
show_index(page=1)
people_search(person)
person_main_info(person_id)
person_cast_credits(person_id)
person_crew_credits(person_id)
show_updates()
```
