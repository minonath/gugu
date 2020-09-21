import ctypes
import timeit

from gu import gu
from gu.system import Array, Type
from gu.opengl import *  # 载入所有显卡绘图的函数
from gu.graphic import *
from gu.window2.mac_font import OCoreFont

gu.window(width=400, height=300)

""" Array """

# Array 构建的主要时间是底层内存数组的构建时间，所以用数组和迭代器时间上是相近的
print('1.1\n新建一个 Float 数组，然后转化为 UByte')
array_0 = Array(*range(4), size=4, data_type=Type.Float)  # bytes = 16
print(array_0)
print(array_0.array_size, array_0.array_bytes, array_0.array_type)
array_0(new_type=Type.UByte)  # 转换
print('\n1.2\n从前一个数组的第 4 位提取 4 个字节组成新的数组')
array_1 = Array.array_at(  # bytes = 4
    array_0.array_offset(4), size=4, data_type=Type.UByte  # 允许 VoidP 或者 LP
)
print(array_0, array_1)
print('\n1.3\n为了证实原始数组和新数组指向的是同一段内存')
array_0[:] = range(16)
print(array_0, array_1)  # 只有第 4 和第 5 个数进行了变换
print('\n1.4\n这时候修改两个数组的任意一个，都会因为指向相同，而互相影响')
array_1.array_from(array_0.array_offset(12))
print(array_0, array_1)
# 过多的构建参数不会影响数组的构建
array_2 = Array(*range(97, 150), size=25, data_type=Type.UByte)  # bytes = 25
print('\n1.5\n可以将 array 转化为 bytes')
print(bytes(array_2))
print(array_2.__bytes__())
print('\n1.6\n获取 offset 的指针')
print(array_0.array_address, array_0.array_offset(0), array_0.array_offset(1))
print('\n1.7\n数组重新赋值')
array_0()
print(array_0)
array_0(0, 0, 0, 0, 99, 99, 99, 99)
print(array_0)
print('=' * 80)

""" Buffer """

print('\n2.1\n构建一个 Buffer 显卡缓存，参数 target 和 mode 表示缓存在显卡内的位置')
buffer_0 = Buffer(array_2, target=Buffer.Array, mode=Buffer.Static)  # 36
print(buffer_0)
print(buffer_0.buffer_bytes, buffer_0.buffer_size, buffer_0.buffer_type)
print('\n2.2\n创建绑定数组，这个 array 和 buffer 具有相当的长度区间，可以用于读取')
# 而且不会和创建 Buffer 用的数组重复
array_buffer_0 = buffer_0.buffer_cache
buffer_0.buffer_read(buffer_0.buffer_cache)
print(array_buffer_0, array_buffer_0 == array_2)
print('\n2.3\n此外，可以创建空的 Buffer 缓存，注意参数含义有变化')
buffer_1 = Buffer(6, Type.UByte, target=Buffer.Array, mode=Buffer.Dynamic)
array_buffer_1 = buffer_1.buffer_cache
buffer_1.buffer_read(array_buffer_1)
print(array_buffer_1)  # 全是空的
print('\n2.4\n测试 Buffer 写入')
assert array_0.array_type == buffer_0.buffer_type  # 需要缓存和数组有相同的类型
buffer_0.buffer_write(array_0, offset=16)  # 长度加偏移可以超过限制
buffer_0.buffer_read(array_buffer_0)
print(array_buffer_0)
print('\n2.5\n改造原有 Buffer 方法一')
buffer_0.buffer_rebuild(array_1)  # 代表着原有缓存失效
print(array_buffer_0 == buffer_0.buffer_cache)  # 尽管依旧能进行读取
buffer_0.buffer_read()  # 这里不再设置临时变量，因为旧的变量会因为改造而失效
print(buffer_0.buffer_cache)  # 但是可以通过 buffer_cache 即时读取
print('\n2.6\n改造原有 Buffer 方法二')
buffer_0.buffer_orphan(30, Type.UByte)  # 代表着原有缓存失效
buffer_0.buffer_read()  # 因为是空缓存，所以可以是任何字符，这里不会进行内存清除
print(buffer_0.buffer_cache)  # 可以看到由于暴力改造而混乱的内存
# 这两个方法都能够重新定义显卡缓存位置
print('\n2.7\n如果在方法二中，调整 target mode 为新的区域，那么就会得到为零的新缓存')
buffer_0.buffer_orphan(36, Type.UByte, mode=Buffer.Dynamic)
buffer_0.buffer_read()
print(buffer_0.buffer_cache)
print('\n2.8\n填写 buffer 缓存，清空内存')
# chunk 也可以是 b'\x01\x02\x03'，只要是 iterable 有意义的数组都可以
buffer_0.buffer_clear(offset=4, length=9, chunk=(1, 2, 3))
buffer_0.buffer_read()
print(buffer_0.buffer_cache)
buffer_0.buffer_clear(offset=4, length=8)
buffer_0.buffer_read()
print(buffer_0.buffer_cache)  # 这里留了一个数字看看效果
print('=' * 80)

""" Texture """

print('\n3.1\n创建一个纹理对象，由于来自图片，数据必须是 bytes 或者 Array')
texture_0 = Texture(array_2, 5, 5, Texture.UInt8)  # 长宽需要注意匹配 5 * 5 = 25
texture_1 = Texture(0, 3, 3, Texture.UInt8)  # 允许空值，但不允许长度不匹配
texture_2 = Texture(b'MEOW', 2, 2, Texture.UInt8)  # 2 * 2 = 4
texture_3 = Texture(None, 16, 16, Texture.Float16, samples=4, depth=True)
print(texture_0)
print(texture_1)
print(texture_2)
print(texture_3)
print(texture_0.texture_compare_function, texture_0.texture_swizzle,
      texture_0.texture_repeat_x, texture_0.texture_repeat_y,
      texture_0.texture_anisotropy, texture_0.texture_viewport,
      texture_0.texture_mag_filter, texture_0.texture_min_filter)
print('\n3.2\n读取纹理对象的内容，多重纹理 samples 不能进行读取')
texture_2.texture_read()
print(texture_2.texture_cache)  # 默认的 cache 是 alignment=1
texture_0.texture_read(alignment=8)  # 当然也可以读其他 alignment 的
print(texture_0.texture_cache)
texture_0.texture_read(buffer_0)  # 也可以读入 buffer 缓存，注意读取用的长度要足够
buffer_0.buffer_read()
print(buffer_0.buffer_cache)  # texture 默认的是 Char 的数组，buffer 默认为 UByte
print('\n3.3写入纹理对象，按照脏矩形更新区域内容')
# 因为之前已经读取了 texture_2.texture_cache 才会有数据
texture_0.texture_write(texture_2.texture_cache, (1, 1, 2, 2))
texture_0.texture_read()
print(texture_0.texture_cache)
print('\n3.4\n改变 Texture 的相关参数')
texture_0.texture_set_compare_function(Compare.Greater)
print(texture_0.texture_compare_function)
texture_0.texture_set_compare_function(None)
texture_0.texture_set_swizzle(Swizzle.Alpha, Swizzle.Alpha)
texture_0.texture_set_repeat_x(False)
texture_0.texture_set_repeat_y(False)
texture_0.texture_set_anisotropy(2.0)
texture_0.texture_set_min_filter(Filter.Nearest)
texture_0.texture_set_mag_filter(Filter.Nearest)
print(texture_0.texture_compare_function, texture_0.texture_swizzle,
      texture_0.texture_repeat_x, texture_0.texture_repeat_y,
      texture_0.texture_anisotropy, texture_0.texture_viewport,
      texture_0.texture_mag_filter, texture_0.texture_min_filter)
print('\n3.5\n创建 Texture 的 mip map')
texture_0.texture_build_mip_maps()
print(texture_0.texture_max_level)
texture_0.texture_cache()  # 清空数组
texture_0.texture_read(level=1)
print(texture_0.texture_cache)
print('=' * 80)

""" Program """

print('\n4.1\n创建一个 Program 显卡程序，为了保证测试，还会有 UniformBlock')
vertex_0 = """#version 410 core
in vec3 test_attribute;
in vec4 test_attribute_array[2];
uniform mat4 test_uniform;
uniform mat4 test_uniform_array[2];
uniform test_block {
    vec3 test_meow_0;
    mat4 test_meow_1;
};
void main() {
    vec4 _t = vec4(test_attribute + test_meow_0, 1.0);
    _t += test_attribute_array[0] + test_attribute_array[1];
    mat4 _m = test_uniform_array[0] + test_uniform_array[1];
    gl_Position = test_uniform * _m * test_meow_1 * _t;
}
"""
program_0 = Program('test_program', GL_VERTEX_SHADER=vertex_0)
print(programs, program_0, program_0.program_member)
print(program_0.test_attribute, program_0.test_uniform, program_0.test_block)
print(program_0.test_attribute_array, program_0.test_uniform_array)
print('\n4.2\n测试 Attribute 的读写')
print(*attribute_get_info(program_0.test_attribute))
print(*attribute_get_info(program_0.test_attribute_array))
print('\n4.3\n测试 Uniform 的读写')
array_3 = Array(*range(32), size=32, data_type=Type.Float)
program_0.test_uniform.uniform_write(array_3)
program_0.test_uniform.uniform_read()
print(program_0.test_uniform.uniform_cache)
program_0.test_uniform_array.uniform_write(array_3)
program_0.test_uniform_array.uniform_read()
print(program_0.test_uniform_array.uniform_cache)
print('\n4.4\n测试 UniformBlock 的读写')
program_0.test_block.uniform_write(array_2, 25)
program_0.test_block.uniform_read()
print(program_0.test_block.uniform_cache)



# b.buffer_write(c, 8)
# x = b.buffer_value_cache
# b.buffer_read(x)
# print(x)
# b.buffer_clear(4, 4, chunk=b'xx1')
# b.buffer_read(x)
# print(x)

# width = height = 16
# data = bytes(range(256))
# c = Array(size=64, data_type=Type.Char)
# t = Texture(data, width, height, Texture.UInt8, 1)
# t.texture_read(t.texture_cache)
# print(bytes(t.texture_cache))
# t.texture_write(c, (8, 8, 8, 8))
# t.texture_read(t.texture_cache)
# print(bytes(t.texture_cache))

# vertex_shader = """#version 330 core
#
# in vec3 gu_position;
# in vec3 gu_color;
# uniform mat4 gu_project_matrix;
# uniform mat4 gu_camera_matrix;
# out vec3 color_0;
#
# void main() {
#     vec4 position_0 = vec4(gu_position, 1.0);
#     vec4 position_1 = gu_camera_matrix * position_0;
#     gl_Position = gu_project_matrix * position_1;
#     color_0 = gu_color;
# }
# """
#
# fragment_shader = """#version 330 core
# out vec4 fragColor;
# in vec3 color_0;
#
# void main()
# {
#     fragColor = vec4(color_0, 1.0);
# }
# """
# p = Program('t03_program', GL_VERTEX_SHADER=vertex_shader,
#                       GL_FRAGMENT_SHADER=fragment_shader)
# print(p)
# uniform = p._program_member['gu_project_matrix']
# cache = uniform.uniform_value_cache
# uniform.uniform_get_value(cache)
# print(cache)


# print('只有开启调试才能输出文本')

# data, width, height = OCoreFont('PingFang', 16).render('咕')
# print(data, width, height)
# print('=' * 80)
# print('使用 gu.system 的 gl_objects 调用显卡对象')
# print('gl_objects =', gl_objects)
# print(texture_1)

# print('=' * 80)
# print('使用 texture_1.gl_destroy() 可以删除对象。')
# print('这是作为显卡对象接口提供的，不建议直接操作显卡对象。')
# print('删除前：gl_objects = ', gl_objects.__dict__)
# texture_1.gl_destroy()
# print('删除后：gl_objects = ', gl_objects.__dict__)
#
# print('=' * 80)
# print('使用 gu.graphic 的 gl_context 查看显卡参数数据')
# print('gu.context =', gl_context)
#
# data = b'\x01\x02\x03\x04\x05\x06\x07\x08'
# data2 = b'\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10'
# texture_1 = Texture(data, 2, 1, Storage.U8, 4)
# result = Array(size=10, data_type=ctypes.c_ubyte)
# texture_1.texture_read(result, write_offset=0)
# print(texture_1)
# print(bytes(result))
#
# result2 = Array(*list(i for i in data2), size=8, data_type=ctypes.c_ubyte)
#
# texture_1.texture_write(result2)
# texture_1.texture_read(result, write_offset=0)
# print(texture_1.texture_ext)
# print(bytes(result))
# texture_1.texture_build_mip_maps()
#
# texture_1.texture_swizzle = Swizzle.ALPHA, Swizzle.ALPHA
# print(texture_1.texture_swizzle)
# texture_1.texture_compare_function = '>'
# print(texture_1.texture_compare_function)
# print(Texture.__dict__)


# def gl_render(interval):
#     glClear(GL_COLOR_BUFFER_BIT)
#     pass
