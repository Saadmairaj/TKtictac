class GuiLoop():
    '''
    This is a Loop that can be used in tkinter applications
    
    Useful the parameters details:- 
        root = 'widget' 
        master = 'function'
        parameters = 'function's parameters'
        count = 'No of times the loop will run'
        speed = 'how fast each loop will run'

    '''
    def __init__(self, root, master, parameters=None, count=True, speed=100):
        self.Brk = False
        self.root = root
        self.master = master
        self.para = parameters
        self.count = count
        self._reset = count
        self.speed = speed
        self.task = ''
        self._Loop()

    def config(self, **options):
        self.master = options.get('master')
        self.count = options.get('count',True)
        self._reset = options.get('count',True)
        self.speed = options.get('speed')

    def _Loop(self):
        if self.__run__() and self.master!=None and not self.Brk:
            if self.para:self.master(self.para)
            else: self.master()
            self.task = self.root.after(self.speed, self._Loop)

    def __run__(self):
        if self.count==True and type(self.count)==bool:
            return True
        elif self.count==False and type(self.count)==bool:
            return False
        if type(self.count)==int:
            if self.count>0:
                self.count-=1
                return True
            else:
                return False
        else:
            print("\nInvaild Entry count can't be {} ,\
                 Either boolean or int".format(self.count))
            
    def StopLoop(self, evt=None):
        self.root.after_cancel(self.task)
        self.count = self._reset
        self.master = None
        self.para = None

    def Pause(self, evt=None):
        self.Brk=True
        self.root.after_cancel(self.task)
        
    def Play(self, evt=None):
        self.Brk=False
        self._Loop()