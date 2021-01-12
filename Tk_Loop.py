class GuiLoop:
    '''
    This is a Loop that can be used in tkinter applications

    Args: 
        root (tk.Widget): Takes the main root window instance. 
        func (function): Takes callback function. 
        parameters (Any): Takes the parameter of the function.
        count (int): No of times the loop should run.
        speed (int): callback function interval (in ms). Deafult is 100ms.
    '''

    def __init__(self, root, func, parameters=None, count=True, speed=100):
        self.Brk = False
        self.root = root
        self.func = func
        self.para = parameters
        self.count = count
        self._reset = count
        self.speed = speed
        self.task = ''
        self._loop()

    def config(self, **options):
        self.func = options.get('func', self.func)
        self.count = options.get('count', self.count)
        self._reset = options.get('count', self._reset)
        self.speed = options.get('speed', self.speed)

    def _loop(self):
        if self.__run__() and self.func != None and not self.Brk:
            if self.para:
                self.func(self.para)
            else:
                self.func()
            self.task = self.root.after(self.speed, self._loop)

    def __run__(self):
        if self.count == True and type(self.count) == bool:
            return True
        elif self.count == False and type(self.count) == bool:
            return False
        if type(self.count) == int:
            if self.count > 0:
                self.count -= 1
                return True
            else:
                return False
        else:
            raise ValueError("\nInvaild Entry count can't be {} ,\
                 Either boolean or int".format(self.count))

    def StopLoop(self, evt=None):
        self.root.after_cancel(self.task)
        self.count = self._reset
        self.func = None
        self.para = None

    def Pause(self, evt=None):
        self.Brk = True
        self.root.after_cancel(self.task)

    def Play(self, evt=None):
        self.Brk = False
        self._loop()
