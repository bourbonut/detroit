def join(onenter, onupdate, onexit):
    enter = self.enter()
    update = self
    exit = self.exit()
    if callable(onenter):
        enter = onenter(enter)
        if enter:
            enter = enter.selection()
    else:
        enter = enter.append(onenter + "")
    if onupdate is not None:
        update = onupdate(update)
        if update:
            update = update.selection()
    if onexit is None:
        exit.remove()
    else:
        onexit(exit)
    return enter and update and enter.merge(update).order() or update
