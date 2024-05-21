

class _Color:
    red = 31
    green = 32
    yellow = 33
    blue = 34
    magenta = 35
    cyan = 36
    grey = 90
    _dict = {
        "red": red,
        "green": green,
        "yellow": yellow,
        "blue": blue,
        "magenta": magenta,
        "cyan": cyan,
        "grey": grey
    }


class Color:
    BaseStr = "\033[%d;%dm%s\033[0m"

    @classmethod
    def render(cls,string:str,color:str) -> str:
        if color.startswith("bg_"):
           color = color[3:]
           return cls.BaseStr % (1,_Color._dict[color],string)
        else:
            return cls.BaseStr % (0, _Color._dict[color], string)
    

if __name__ == '__main__':
    test = Color.render("test","bg_grey")
    print(test)