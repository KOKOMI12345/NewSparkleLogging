

class _Color:
    red = 31
    green = 32
    yellow = 33
    blue = 34
    magenta = 35
    cyan = 36
    write = 37
    grey = 90
    background_red = 41


class Color:
    BaseStr = "\033[%d;%dm%s\033[0m"

    @classmethod
    def render(cls,string:str,color:str) -> str:
        if color.startswith("bd_"):
           color = color[3:]
           return cls.BaseStr % (1,_Color.__dict__[color],string)
        else:
            return cls.BaseStr % (0, _Color.__dict__[color], string)
    

if __name__ == '__main__':
    test = Color.render("test","bd_background_red")
    print(_Color.__dict__)