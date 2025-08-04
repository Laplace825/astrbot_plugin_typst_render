import typst
import tempfile
import os

from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.core.config.astrbot_config import AstrBotConfig
from astrbot.api import logger


@register(
    "astrbot_plugin_typst_render", 
    "Laplace", 
    "渲染Typst代码并返回图片", 
    "0.1.1",
    "https://github.com/Laplace825/astrbot_plugin_typst_render")
class TypstRenderPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.math_font_size = config.get("math_font_size", "14pt")
        self.math_height = config.get("math_height", "auto")

    @staticmethod
    def __typ_render_core(source: str) -> str:
        """
        渲染Typst代码并返回图片路径
        :param source: Typst代码字符串
        :return: 渲染后的图片路径
        """
        temp_png_file_dir = tempfile.TemporaryDirectory()
        temp_typst_file = tempfile.NamedTemporaryFile(suffix=".typst", delete=False)
        # 将Typst代码写入临时文件
        with open(temp_typst_file.name, "w", encoding='utf-8') as f:
            f.write(source)
        logger.info(f"Typst code 临时保存到 {temp_typst_file.name}")
        random_png_file_name = f"{temp_typst_file.name}.png"
        typst.compile(
            temp_typst_file.name,
            output=os.path.join(temp_png_file_dir.name, random_png_file_name),
            format="png",
        )
        logger.info(f"Typst 图片临时保存到 {temp_png_file_dir.name}/{random_png_file_name}")
        return os.path.join(temp_png_file_dir.name, random_png_file_name)

    # 注册指令的装饰器。指令名为 tym。注册成功后，发送 `/tym` 就会触发这个指令, 专门渲染数学公式
    @filter.command("tym")
    async def on_command_tym(self, event: AstrMessageEvent):
        message_str = event.message_str  # 用户发的纯文本消息字符串
        message_str = message_str[3:]
        if not message_str:
            yield event.plain_result("请提供Typst公式进行渲染")
            return
        message_str = f"{self.__gen_math_style(self.math_font_size, self.math_height)}\n{message_str}"
        yield event.image_result(
            self.__typ_render_core(message_str),
        )

    @filter.command("typ")
    async def on_command_typ(self, event: AstrMessageEvent):
        message_str = event.message_str
        message_str = message_str[3:]
        if not message_str:
            yield event.plain_result("请提供Typst代码进行渲染")
            return
        yield event.image_result(
            self.__typ_render_core(message_str),
        )

    @filter.command("yau")
    async def on_command_yau(self, event: AstrMessageEvent):
        message_str = event.message_str
        message_str = message_str[3:]
        if not message_str:
            yield event.plain_result("请提供Typst OurChat代码进行渲染")
            return
        message_str = f"{self.__gen_ourchat()}\n{message_str}"
        yield event.image_result(
            self.__typ_render_core(message_str),
        )

    @staticmethod
    def __gen_math_style(math_font_size, math_height) -> str:
        """
        生成数学公式的Typst样式, 便于阅读
        :return: Typst样式字符串
        """
        return f"""
#show math.equation: it => {{
  set text(size: {math_font_size})
  set page(margin: auto, height: {math_height})
  set align(center + horizon)
  it
}}
        """

    @staticmethod
    def __gen_ourchat() -> str:
        """
        生成OurChat样式的Typst样式
        :return: OurChat样式字符串
        """
        return """
#import "@preview/ourchat:0.2.0" as oc
#import oc.themes: *
#set page(margin: auto, height: auto, width: auto)
#let yau = wechat.default-user(name: [丘成桐（囯內）])
        """