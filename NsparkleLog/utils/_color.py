import re

class _Color:
    red = 31
    green = 32
    yellow = 33
    blue = 34
    magenta = 35
    cyan = 36
    white = 37
    grey = 90
    background_red = 41

class Color:
    BaseStr = "\033[%d;%dm%s\033[0m"

    @classmethod
    def GetAvaliableColor(cls) -> list:
        return [i for i in _Color.__dict__ if not i.startswith("__")]

    @classmethod
    def regColor(cls,colorCode: int,colorName: str) -> None:
        setattr(_Color,colorName,colorCode)

    @classmethod
    def render(cls,string:str,color:str) -> str:
        if color.startswith("bd_"):
           color = color[3:]
           return cls.BaseStr % (1,_Color.__dict__[color],string)
        else:
            return cls.BaseStr % (0, _Color.__dict__[color], string)
        
    @classmethod
    def renderByHtml(cls, string: str) -> str:
        """
        一个接口让你允许用HTML标签来渲染颜色
        """
        pattern = re.compile(r"<(\w+)>(.*?)</\1>", re.DOTALL)
        while True:
            match = pattern.search(string)
            if not match:
                break
            color_tag = match.group(1)
            inner_text = match.group(2)
            ansi_code = cls.render(inner_text, color_tag)
            string = string[:match.start()] + ansi_code + string[match.end():]
        return string
    
    

if __name__ == '__main__':
    test = Color.renderByHtml("<red>hello</red> <bd_blue>world</bd_blue>")
    print(test)