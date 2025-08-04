import typst
import tempfile
import os

from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger


@register("TypstRender", "Laplace", "渲染Typst代码并返回图片", "0.0.1")
class TypstRender(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # 注册指令的装饰器。指令名为 typ。注册成功后，发送 `/typ` 就会触发这个指令
    @filter.command("typ")
    async def typ(self, event: AstrMessageEvent):
        self.temp_png_file_dir = tempfile.TemporaryDirectory()
        message_str = event.message_str  # 用户发的纯文本消息字符串
        if not message_str:
            yield event.plain_result("请提供Typst代码进行渲染")
        random_png_file_name = f"{event.get_session_id()}.png"
        typst.compile(
            message_str,
            output=os.path.join(self.temp_png_file_dir.name, random_png_file_name),
            format="png",
        )
        logger.info(f"Typst code rendered to {random_png_file_name} in temp directory.")
        yield event.image_result(
            os.path.join(self.temp_png_file_dir.name, random_png_file_name),
        )

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
