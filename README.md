Basic single-show usage

```python
import pytvmaze

show = pytvmaze.get_show('dexter')
print show
>>> <pytvmaze.Show instance at 0x107abefc8>
print show.name, show.status, show.maze_id
>>> Dexter Ended 161

ep = show.get_episode(1,8)
print ep
>>> <pytvmaze.Episode instance at 0x107b060e0>
print ep.title
>>> Shrink Wrap

```

See pytvmaze.py for all available properties of the Show() and Episode() classes (there are many).

Aside from these classes, you can also utilize all of the TV Maze endpoints directly via their respective functions.  There are many endpoints, see pytvmaze.py for all of them.  The results of these functions are JSON.  Here are a few examples:

```python
show_search(show) # returns a list of fuzzy-matched shows given a show name (string)
show_single_search(show) # returns the best-matched show
show_single_search(show, embed=[option]) # see http://www.tvmaze.com/api#embedding for embedding other information in your results
lookup_tvdb(tvdb_id) # get tvmaze show data from a tvdb show id
```
