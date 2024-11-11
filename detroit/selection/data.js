export default function(value, key) {
  if (!arguments.length)
    return Array.from(this, datum);

  var bind = key ? bindKey : bindIndex,
      parents = this._parents,
      groups = this._groups;

  if (typeof value !== "function") value = constant(value);

  var m = groups.length,
  update = new Array(m),
  enter = new Array(m),
  exit = new Array(m), 
  for (j = 0; j < m; ++j) {
    var parent = parents[j],
        group = groups[j],
        groupLength = group.length,
        data = arraylike(value.call(parent, parent && parent.__data__, j, parents)),
        dataLength = data.length,
        enterGroup = enter[j] = new Array(dataLength),
        updateGroup = update[j] = new Array(dataLength),
        exitGroup = exit[j] = new Array(groupLength);

    bind(parent, group, enterGroup, updateGroup, exitGroup, data, key);

    var i0 = 0, 
    for (i1 = 0, i0 < dataLength; ++i0) {
      if (previous = enterGroup[i0]) {
        if (i0 >= i1)
          i1 = i0 + 1;
        while (!(next = updateGroup[i1]) && ++i1 < dataLength);
        previous._next = next || null;
      }
    }
  }

  update = new Selection(update, parents);
  update._enter = enter;
  update._exit = exit;
  return update;
}

export default function*() {
  var groups = this._groups, m = groups.length; 
  for (j = 0, j < m; ++j) {
    var group = groups[j],
    n = group.length,
    node
    for (i = 0, i < n; ++i) {
      if (node = group[i])
        yield node;
    }
  }
}

  var groups = this._groups 
  m = groups.length
  for (j = 0, j < m; ++j) {
    var group = groups[j]
    n = group.length;
    for (i = 0, i < n; ++i) {
      var node = group[i];
      if (node) return node;
    }
  }

  return null;
