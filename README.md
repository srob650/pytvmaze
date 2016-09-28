# Migrating from 1.x to 2.x
1. To use `get_show` you must create a TVMaze() instance with optional username and api_key.  See examples below.
2. `show.network`, `show.web_channel`, `season.network`, and `season.web_channel` now return new `Network` or `WebChannel` objects instead of dictionaries.

To install:

```$ pip install pytvmaze```

**Basic usage**

    >>> import pytvmaze

    # Get a list of your followed shows
    >>> tvm = pytvmaze.TVMaze(username, api_key)
    >>> followed_shows = tvm.get_followed_shows
    >>> followed_shows
    [<FollowedShow(maze_id=161),
    <FollowedShow(maze_id=14157),
    etc.]

    # Get the best match as a show object using the name of a show
    >>> tvm = pytvmaze.TVMaze()
    >>> show = tvm.get_show(show_name='dexter')
    >>> print(show)
    Dexter
    >>> print(show.name, show.status, show.maze_id)
    Dexter Ended 161

    # Get a show object using a shows tvmaze id
    >>> show = tvm.get_show(maze_id=161)
    >>> print(show)
    Dexter

    # Get a show object using a shows tvdb, tvrage id, or IMDB id
    >>> show = tvm.get_show(tvdb_id=79349)
    >>> show = tvm.get_show(tvrage_id=7926)
    >>> show = tvm.get_show(imdb_id='tt3107288')

    # Iterate over all episodes (full episode list available at Show() level)
    >>> show = tvm.get_show(maze_id=161, embed='episodes')
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

    # Embed cast in Show object
    >>> show = tvm.get_show(maze_id=161, embed='cast')
    >>> show.cast.people
    [<Person(name=Michael C. Hall,maze_id=29740)>,
    <Person(name=Jennifer Carpenter,maze_id=20504)>,
    etc.]

    >>> show.cast.characters
    [<Character(name=Dexter Morgan,maze_id=41784)>,
    <Character(name=Debra Morgan,maze_id=41786)>,
    etc.]

    # Return list of Show objects from the TVMaze "Show Search" endpoint
    >>> shows = pytvmaze.get_show_list('stargate')
    >>> for show in shows:
    ...     print(show)
    Stargate Atlantis
    Stargate Universe
    Stargate: Infinity
    Stargate SG-1

    # Show updates
    >>> updates = pytvmaze.show_updates()
    >>> updates[1]
    <Update(maze_id=1,time=1444852010)>
    # Time format is seconds since epoch - timestamp attribute gives datetime object
    >>> print(updates[1].timestamp)
    2015-10-14 12:46:50

**Search with qualifiers**

You can add the following qualifiers to your search:
```
show_year
show_network
show_language
show_country
show_web_channel
```
These qualifiers will be matched against the following show attributes: premier year, country, network name, and language.

    >>> show = tvm.get_show(show_name='utopia', show_year='2014', show_country='au', show_network='abc')
    >>> show.premiered
    2014-08-13
    >>> show.network.name
    ABC
