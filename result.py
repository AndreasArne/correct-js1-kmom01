import pyperclip

class Result:
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Result.__instance == None:
            Result()
            return Result.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Result.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Result.__instance = self
        
        self.lab = ""
        self.links = ""
        self.unicorn = ""
        self.jsfiddle = ""
        self.redovisa = []
        self.github = ""

    def __repr__(self):
        res = """{lab}
{links}
{unicorn}
{jsfiddle}
{redovisa}
{github}""".format(
                lab=self.lab,
                links=self.links,
                unicorn=self.unicorn,
                jsfiddle=self.jsfiddle,
                redovisa="\n".join(self.redovisa),
                github=self.github
            )
        return res
    
    def __str__(self):
        return self.__repr__()
    
    def copy_text(self):
        pyperclip.copy(self.__repr__())