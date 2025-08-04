import typst
import tempfile
import os
import base64
import asyncio

from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.core.config.astrbot_config import AstrBotConfig
from astrbot.api import logger


@register(
    "astrbot_plugin_typst_render", 
    "Laplace", 
    "渲染Typst代码并返回图片", 
    "0.2.0",
    "https://github.com/Laplace825/astrbot_plugin_typst_render")
class TypstRenderPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.math_font_size = config.get("math_font_size", "14pt")
        self.math_height = config.get("math_height", "auto")

    @staticmethod
    async def __typ_render_core(source: str) -> str:
        """
        渲染Typst代码并返回图片的base64编码
        :param source: Typst代码字符串
        :return: 图片的base64编码字符串
        """
        # 创建临时文件来存储Typst代码
        with tempfile.NamedTemporaryFile(mode='w', suffix=".typst", delete=False, encoding='utf-8') as temp_typst_file:
            temp_typst_file.write(source)
            temp_typst_file.flush()
            temp_typst_path = temp_typst_file.name
        
        try:
            # 使用 asyncio.to_thread 在独立线程中执行阻塞的 typst.compile 操作
            # 避免阻塞主事件循环，保持并发性能
            img_bytes = await asyncio.to_thread(
                typst.compile,
                temp_typst_path,
                format="png"
            )
            
            # 转换为base64编码
            base64_str = base64.b64encode(img_bytes).decode('utf-8')
            logger.info("图片已转换为base64编码")
            return base64_str
        finally:
            # 清理临时文件
            try:
                os.unlink(temp_typst_path)
            except OSError:
                logger.warning(f"无法删除临时文件: {temp_typst_path}")

    # 注册指令的装饰器。指令名为 tym。注册成功后，发送 `/tym` 就会触发这个指令, 专门渲染数学公式
    @filter.command("tym")
    async def on_command_tym(self, event: AstrMessageEvent):
        message_str = event.message_str  # 用户发的纯文本消息字符串
        message_str = message_str[len("tym"):]
        if not message_str:
            yield event.plain_result("请提供Typst公式进行渲染")
            return
        message_str = f"{self.__gen_math_style(self.math_font_size, self.math_height)}\n{message_str}"
        base64_image_data = await self.__typ_render_core(message_str)
        yield event.make_result().base64_image(base64_image_data)

    @filter.command("typ")
    async def on_command_typ(self, event: AstrMessageEvent):
        message_str = event.message_str
        message_str = message_str[len("typ"):]
        if not message_str:
            yield event.plain_result("请提供Typst代码进行渲染")
            return
        base64_image_data = await self.__typ_render_core(message_str)
        yield event.make_result().base64_image(base64_image_data)

    @filter.command("yau")
    async def on_command_yau(self, event: AstrMessageEvent):
        message_str = event.message_str
        message_str = message_str[len("yau"):]
        if not message_str:
            yield event.plain_result("请提供Typst OurChat代码进行渲染")
            return
        message_str = f"{self.__gen_ourchat()}\n{message_str}"
        base64_image_data = await self.__typ_render_core(message_str)
        yield event.make_result().base64_image(base64_image_data)

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