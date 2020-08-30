import tkinter as tk


def _agsmerge(args):
    """Internal functions.\n
    Merges lists/tuples."""
    a = []
    if isinstance(args, (tuple, list)):
        for i in args:
            if isinstance(i, (tuple, list)):
                a.extend(i)
            else:
                a.append(i)
    return a or args


# Define Grid layout
def grid(root, row, column):
    "Defines rows and columns if grid method is used"
    if column:
        for y in range(column):
            tk.Grid.columnconfigure(root, y, weight=1)
    if row:
        for x in range(row):
            tk.Grid.rowconfigure(root, x, weight=1)


class Canvas(tk.Canvas):

    def create_roundsqaure(self, ags=(), *args, **kw):
        'Internal function.'
        x, y, w, h, c = _agsmerge((ags, args))
        ids = []
        cnf = dict(kw)
        for i in ('extent', 'start', 'style'):
            cnf.pop(i, None)
        for i in ('joinstyle', 'smooth', 'slinesteps'):
            kw.pop(i, None)
        points = (  # Arc points:-
            (x, y, x+2*c, y+2*c),
            (x, y+h-2*c, x+2*c, y+h),
            (x+w-2*c, y+h-2*c, x+w, y+h),
            (x+w-2*c, y, x+w, y+2*c),
            # Polygon points:-
            (x+c, y, x+w-c, y),
            (x+c, y+h, x+w-c, y+h),
            (x, y+c, x, y+h-c),
            (x+w, y+c, x+w, y+h-c))

        for i in range(len(points)):
            if i <= 3:
                kw['start'] = 90*(i+1)
                ids.append(self._create('arc', points[i], kw))
            else:
                ids.append(self._create('polygon', points[i], cnf))
        return tuple(ids)

    # Circle for the canvas
    def create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
