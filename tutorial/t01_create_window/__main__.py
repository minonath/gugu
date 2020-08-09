#  即使什么也不做也会开启一个窗口。
from gu import gu
from gu.system import default_png  # 默认图标。

gu.window(title='tutorial 01')  # 修改窗口名称。
gu.window(width=400, height=300)  # 修改窗口尺寸，可以多个参数一起写。
gu.window(image=default_png)  # 修改窗口图标，不修改的话是 python 的火箭图标。
gu.window(fps=24)  # 修改刷新率。
