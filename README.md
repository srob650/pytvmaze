Basic single-show usage

'''python
show = get_show('dexter')
print show.name, show.status, show.maze_id
>>> Dexter Ended 161

print show.get_episode(1,8).name
>>> Shrink Wrap

'''

