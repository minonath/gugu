from gu import gu
from gu.opengl import *  # 载入所有显卡绘图的函数
from gu.graphic import Texture
from gu.window.mac_font import OCoreFont


gu.window(width=400, height=300)


def gl_init():
    print('只有开启调试才能输出文本')

    data, width, height = OCoreFont('PingFang', 16).render('咕')
    Texture(data, width, height, 'unsigned 8', 1)

    print('=' * 80)
    print('使用 gu.context.objects 调用显卡对象')
    print('gu.context.objects.texture_1 =')
    print(gu.context.objects.texture_1)

    print('=' * 80)
    print('使用 del gu.context.objects.texture_1 可以删除对象。')
    print('这是作为显卡对象接口提供的，不建议直接操作显卡对象。')
    print('删除前：gu.context.objects = ', gu.context.objects.__dict__)
    del gu.context.objects.texture_1
    print('删除后：gu.context.objects = ', gu.context.objects.__dict__)


def gl_clear():
    glClear(GL_COLOR_BUFFER_BIT)


def gl_render(interval):
    pass


gu.context.gl_init = gl_init
gu.context.gl_clear = gl_clear
gu.context.gl_render = gl_render
