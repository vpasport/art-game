from PIL import Image
from termcolor import colored
from pprint import pprint
from colorutils import Color, ArithmeticModel
from math import sqrt, atan
import api
from time import sleep


def check_current():
    info = api.get_info()

    if (info['status'] == 200):
        image = Image.open(api.get_image_bytes(
            info['response']['canvas']['url']))
        image.save('./curr.png')

        width, height = image.size
        print(colored('image size: ', 'blue'),
              colored(f'[{height}, {width}] - [h, w]', 'yellow'))

        colors = [[None for w in range(width)] for h in range(height)]

        for h in range(0, height, 1):
            for w in range(0, width, 1):
                colors[h][w] = Color(
                    image.getpixel((w, h)),  arithmetic=ArithmeticModel.BLEND)

        return colors


def load_image():
    image = Image.open('../images/2.png')
    width, height = image.size
    print(colored('image size: ', 'blue'),
          colored(f'[{width}, {height}] - [w, h]', 'yellow'))

    colors = [[None for w in range(width)] for h in range(height)]

    for h in range(0, height, 1):
        for w in range(0, width, 1):
            colors[h][w] = Color(
                image.getpixel((w, h)),  arithmetic=ArithmeticModel.BLEND)

    return colors


def save_image(colors_arr, name='image'):
    img = Image.new('RGB', [len(colors_arr[0]), len(colors_arr)], 255)
    data = img.load()

    for h in range(0, len(colors_arr), 1):
        for w in range(0, len(colors_arr[0]), 1):
            data[w, h] = colors_arr[h][w].rgb

    img.save(name + '.png')


def unpack_rgb(color):
    r = 0xFF & (color >> 16)
    g = 0xFF & (color >> 8)
    b = 0xFF & color
    return r, g, b


def test(color, image, current_image, count, save_image_name=None):
    colors_arr = [[None for w in range(len(image[0]))]
                  for h in range(len(image))]

    # white = sqrt((255) ** 2+(255) ** 2+(255) ** 2)

    def d(c1, c2):
        r1, g1, b1 = c1.rgb
        r2, g2, b2 = c2.rgb

        return sqrt((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2)

    # def p(d):
    #     return d / white

    distances = []

    for h in range(0, len(image), 1):
        for w in range(0, len(image[0]), 1):
            r, g, b = image[h][w]
            if (r == 255 and g == 255 and b == 255):
                continue
            d_img = d(image[h][w], color)
            d_curr = d(current_image[h][w], color)
            if (d_img < d_curr):
                distances.append({
                    'positions': {
                        'h': h,
                        'w': w
                    },
                    'distance': d_img,
                })

    distances = sorted(distances, key=lambda d: d['distance'])[
        0:count]

    if (save_image_name != None):
        save_image(colors_arr, save_image_name)

    return distances

# x - w
# y - h


def shoot_calc(h, w, image_w, image_h):
    # 425 = ((ma) ^ 2 * sin(2 *45)) / 9.80665
    # 425 = (m^2 a^2 * 0.8939966636) / 9.80665
    # 4167.82625 = m^2 a^2 * 0.8939966636
    # 4662.015441105501 = m^2 a^2

    # L = 2v₀²sin(α)cos(α) / g
    # 425 = 2 v^2 * 0.8509035245341184 * 0.5253219888177297 / 9.80665
    # 4167.82625 = 2 v^2 * 0.8509035245341184 * 0.5253219888177297
    # 4662.0154411025915 = v^2
    #
    # F = ma = m (v^2 - u^2) / (2s)
    # F = 1 (v^2) / 2s
    # F = 4662.0154411025915 / 850
    # F = 5.48472404835599
    #
    #
    #
    # s = (v^2 /g) * sin(2 * 45)
    # v = 64.56Начальная скорость (м/с):

    # a = (v * sin(α)) / t,
    # t = (2 * v * sin(α)) / g
    # a = (v * sin(α)) / (2 * v * sin(α)) / g
    # a = 54.93433154392269 / 109.86866308784538 / 9.80665
    # a = 0.050985810648896415

    cat1 = abs(image_w / 2 - w)
    cat2 = 300 + h
    # cat2 = 300 + h

    # 340 = 2
    # 200 / 340

    # force = (340 / sqrt(cat1 ** 2 + cat2 ** 2)) / 0.5
    force = sqrt(cat1 ** 2 + cat2 ** 2) / 170

    # angle = atan(cat1 / cat2) * 180 / 3.1415926535898
    angle = atan(cat2 / cat1)
    print(cat1, cat2, angle)

    return {
        'angleHorizontal': '{:.6f}'.format(-angle if w < image_w / 2 else angle),
        'angleVertical': 45,
        'power': '{:.6f}'.format(force)
    }


image = load_image()
sended_image = [[Color((255, 255, 255)) for w in range(len(image[0]))]
                for h in range(len(image))]


def main():
    curr_img = check_current()

    # colors = [[None for w in range(len(image[0]))] for h in range(len(image))]

    # for h in range(0, len(image), 1):
    #     for w in range(0, len(image[0]), 1):
    #         colors[h][w] = image[h][w] + curr_img[h][w]

    # save_image(colors)

    color_list = api.get_colors_list()
    pprint(color_list)
    if (len(color_list['response']) == 0):
        # if (True):
        new_colors_response = api.generate_colors()
        tick = new_colors_response['info']['tick']
        colors = new_colors_response['response']

        min_dist = float('inf')
        min_color = ''
        min_color_key = ''
        coords = []

        for key in colors:
            color = Color(unpack_rgb(colors[key]['color']),
                          arithmetic=ArithmeticModel.BLEND)
            res = test(color, image, curr_img, colors[key]['amount'])

            print(res)

            if (res[0]['distance'] < min_dist):
                min_dist = res[0]['distance']
                min_color_key = key
                coords = res
                min_color = colors[key]['color']

        print(coords)

        res = api.pick_color(min_color_key, tick)

        sleep(0.2)

        for i in range(len(coords)):
            shoot_data = shoot_calc(
                coords[i]['positions']['h'], coords[i]['positions']['w'],  len(image), len(image[0]))
            shoot_data[f'colors[{min_color}]'] = 1

            shoot = api.shoot(shoot_data)
            pprint(shoot_data)
            pprint(shoot)
            if (shoot['status'] == 200):
                sended_image[coords[i]['positions']
                             ['h']][coords[i]['positions']['w']] = Color(unpack_rgb(min_color))

            sleep_time = shoot['info']['ns'] / (10 ** 9)
            print(colored(f'sleep {sleep_time}s', 'blue'))

            if (sleep_time > 0):
                sleep(sleep_time)
    else:
        min_dist = float('inf')
        min_color = ''
        coords = []

        for key in color_list['response']:
            color = Color(unpack_rgb(int(key)),
                          arithmetic=ArithmeticModel.BLEND)

            res = test(color, image, curr_img,  color_list['response'][key])

            if (res[0]['distance'] < min_dist):
                min_dist = res[0]['distance']
                coords = res
                min_color = key

        for i in range(len(coords)):
            shoot_data = shoot_calc(
                coords[i]['positions']['h'], coords[i]['positions']['w'],  len(image), len(image[0]))
            shoot_data[f'colors[{min_color}]'] = 1

            # continue
            shoot = api.shoot(shoot_data)
            pprint(shoot_data)
            pprint(shoot)
            if (shoot['status'] == 200):
                sended_image[coords[i]['positions']
                             ['h']][coords[i]['positions']['w']] = Color(unpack_rgb(min_color))

            sleep_time = shoot['info']['ns'] / (10 ** 9)
            print(colored(f'sleep {sleep_time}s', 'blue'))
            if (sleep_time > 0):
                sleep(sleep_time)

    save_image(sended_image, 'sanded')


for i in range(100):
    main()
