Basic single-show usage

```python
import pytvmaze

show = pytvmaze.get_show('dexter')
print show
```>>> <pytvmaze.Show instance at 0x107abefc8>```
print show.name, show.status, show.maze_id
```>>> Dexter Ended 161```

ep = show.get_episode(1,8)
print ep
```>>> <pytvmaze.Episode instance at 0x107b060e0>```
print ep.name
```>>> Shrink Wrap```

```

See pytvmaze.py for all available properties of the Show() and Episode() classes (there are many).
