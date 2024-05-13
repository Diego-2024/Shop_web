import random
import string
from PIL import Image, ImageFont, ImageDraw

def rndColor():
    '''随机颜色'''
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def gene_text():
    '''生成4位验证码'''
    return ''.join(random.sample(string.ascii_letters + string.digits, 4))


def draw_lines(draw, num, width, height):
    '''划线'''
    for num in range(num):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, height / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(height / 2, height)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)


def get_verify_code():
    '''生成验证码图形'''
    code = gene_text()
    # 图片大小120×50
    width, height = 120, 50
    # 新图片对象
    im = Image.new('RGB', (width, height), 'white')
    # 字体
    font = ImageFont.truetype('app/static/fonts/arial.ttf', 40)
    # draw对象
    draw = ImageDraw.Draw(im)
    # 添加干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=2)
    # 添加干扰点
    for i in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(0, 0, 0))
    # 绘制字符串
    for item in range(4):
        draw.text((5 + random.randint(-3, 3) + 23 * item, 5 + random.randint(-3, 3)),
                  text=code[item], fill=rndColor(), font=font)
    return im, code