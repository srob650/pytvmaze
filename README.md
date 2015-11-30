### **Notice**
 - Updated get_show() method to require explicit embedding of episodes
 - Plan to add other embeds in future commit such as cast, nextepisode,  and previousepisode

To install:

```$ pip install pytvmaze```

**Basic usage**

    >>> import pytvmaze

    # Return list of Show objects from the TVMaze "Show Search" endpoint
    >>> shows = pytvmaze.get_show_list('stargate')
    >>> for show in shows:
    ...     print(show)
    Stargate Atlantis
    Stargate Universe
    Stargate: Infinity
    Stargate SG-1

    # Get the best match as a show object using the name of a show
    >>> show = pytvmaze.get_show(show_name='dexter')
    >>> print(show)
    Dexter
    >>> print(show.name, show.status, show.maze_id)
    Dexter Ended 161

    # Get a show object using a shows tvmaze id
    >>> show = pytvmaze.get_show(maze_id=161)
    >>> print(show)
    Dexter

    # Get a show object using a shows tvdb or tvrage id
    >>> show = pytvmaze.get_show(tvdb_id=79349)
    >>> show = pytvmaze.get_show(tvrage_id=7926)

    # Iterate over all episodes (full episode list available at Show() level)
    >>> show = pytvmaze.get_show(maze_id=161, embed='episodes')
    >>> for episode in show.episodes:
    ...     print(episode.title)
    Dexter
    Crocodile
    Popping Cherry
    etc...

    # You can also use:
    >>> for season in show:
    ...     for episode in season:
    ...         ...

    # Iterate over specific season (season 2 for example)
    >>> for episode in show[2]:
    ...     print(episode.title)
    It's Alive!
    Waiting to Exhale
    An Inconvenient Lie
    etc...

    # Get a specific episode with: show[season][episode]
    >>> ep = show[1][8]
    >>> print(ep)
    S01E08 Shrink Wrap
    >>> print(ep.title)
    Shrink Wrap

**Search with qualifiers**

You can add the following qualifiers to your search:
```
show_year
show_network
show_language
show_country
```
These qualifiers will be matched against the following show attributes: premier year, country, network name, and language.

    >>> show = pytvmaze.get_show(show_name='utopia', show_year='2014', show_country='au', show_network='abc')
    >>> show.premiered
    2014-08-13
    >>> show.network['name']
    ABC

**Show() Season() and Episode() class attributes**

There are many possible attributes of the Show class, but since TV Maze is full of user contributions and always being updated, shows will have different available attributes.  Possible attributes are:

    ## Show object attributes ##
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
    show.seasons # dict of Season objects

    ## Season object attributes ##
    season.show # the parent show object
    season.season_number
    season.episodes # dict of episodes within this season

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

**Direct api.tvmaze.com endpoint access**

Aside from these classes, you can also utilize all of the TV Maze endpoints directly, without creating an insance of the Show class, via their respective functions.  The results of these functions are JSON:

    pytvmaze.show_search(show) # returns a list of fuzzy-matched shows given a show name (string)
    pytvmaze.show_single_search(show) # returns the best-matched show
    pytvmaze.show_single_search(show, embed=[option]) # see http://www.tvmaze.com/api#embedding for embedding other information in your results
    pytvmaze.lookup_tvrage(tvrage_id) # get tvmaze show data from a tvrage show id
    pytvmaze.lookup_tvdb(tvdb_id) # get tvmaze show data from a tvdb show id
    pytvmaze.get_schedule(country='US')
    pytvmaze.get_full_schedule() # ALL future known episodes.  Several MB large, cached for 24 hours
    pytvmaze.show_main_info(maze_id)
    pytvmaze.episode_list(maze_id)
    pytvmaze.episode_by_number(maze_id, season_number, episode_number)
    pytvmaze.episodes_by_date(maze_id, airdate) # returns a list of all episodes that show aired on that day, airdate must be ISO 8601 formatted
    pytvmaze.show_cast(maze_id)
    pytvmaze.show_index(page=1)
    pytvmaze.people_search(person)
    pytvmaze.person_main_info(person_id)
    pytvmaze.person_cast_credits(person_id)
    pytvmaze.person_crew_credits(person_id)
    pytvmaze.show_updates()
    pytvmaze.show_akas(maze_id)
