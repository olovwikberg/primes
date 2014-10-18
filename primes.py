#!/Users/olov/Envs/primes/bin/python

import math
from datetime import datetime

sign = lambda x: math.copysign(1, x) 

def factors(n):    
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def get_primes(n):
    numbers = set(range(n, 1, -1))
    primes = []
    while numbers:
        p = numbers.pop()
        primes.append(p)
        numbers.difference_update(set(range(p*2, n+1, p)))
    return primes

def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

twoPi = 2*math.pi

def coordinate_archimedes(n):
    sqrt_n = math.sqrt(n)

    return (sqrt_n * math.cos(sqrt_n * twoPi), sqrt_n * math.sin(sqrt_n * twoPi))
def coordinate_square(n):
    if n < 1:
        raise Exception("n must be positive!")
    elif n == 1:
        return (0, 0)


    n_isqrt = isqrt(n)
    highest_sqr = n_isqrt*n_isqrt
    # if equal square root
    if highest_sqr == n:
        # if odd equal square root
        if n % 2:
            return ((n_isqrt - 1) / 2, (n_isqrt - 1) / 2)
        # if even equal square root
        else:
            return (-(n_isqrt) / 2 + 1, -n_isqrt / 2)
    else:
        c = coordinate_square(highest_sqr)
        rest = n - highest_sqr
        # if odd
        if highest_sqr % 2:
            return (c[0] + 1 - max(rest - n_isqrt - 1, 0), c[1] - min(rest - 1, n_isqrt))
        else:
            return (c[0] - 1 + max(rest - n_isqrt - 1, 0), c[1] + min(rest - 1, n_isqrt))

def calculateDotImage():
    from PIL import Image, ImageDraw
    
    measure=8268 # 70cmx70cm,300 dpi
    # measure=2000
    spacing = 4
    scale = 2
    coordinate_function=coordinate_archimedes

    # Dark and blue
    # color=(117, 180, 224)
    # color2=color
    # backgroundColor=(52, 52, 52)

    # newspaper
    color=(10, 10, 9)
    color2=color
    backgroundColor=(244, 244, 226)

    # measure=2000
    # spacing = 7
    # scale = 4
    # coordinate_function=coordinate_square
    # color=(117, 180, 224)
    # color2=(color[0]/2, color[1]/2, color[2]/2)

    size = (measure, measure)
    image = Image.new('RGB', size)
    center = (size[0] / 2, size[1] / 2)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0) + size, fill=backgroundColor)
    n_max = int(0.9 * measure * measure / (scale * scale * spacing * spacing))
    # primes=get_primes(n_max)
    # for n in primes:
    for n in range(1, n_max+1):
    	# scale e.g. 1
        # c=coordinate_archimedes(n)
        c=coordinate_function(n)
        pos=(scale*spacing*c[0]+center[0], scale*spacing*c[1]+center[0])

        # use spacing = 1
        # k = max(255-len(factors(n))*50, 0)
        # image.putpixel(pos, (k, k, k))
        len_factors = len(factors(n))
        scale_len_factors=scale*math.sqrt(len_factors)
        ellipse_poss=(pos[0] - scale_len_factors / 2, pos[1] - scale_len_factors / 2, pos[0] + scale_len_factors / 2, pos[1] + scale_len_factors / 2)

        # original colors
        draw.ellipse(ellipse_poss, fill = color, outline =color2)

        # fun colors
        # if len_factors>20:
        # 	a_color = (255, 0, 0)
        # elif len_factors>16:
        # 	a_color = (255, 255, 0)
        # elif len_factors>12:
        # 	a_color = (0, 255, 0)
        # elif len_factors>8:
        # 	a_color = (0, 255, 255)
        # elif len_factors>4:
        # 	a_color = (0, 0, 255)
        # else:
        # 	a_color = (255, 0, 255)
        # draw.ellipse(ellipse_poss, fill = a_color, outline = a_color)

        if n % 1000 == 0:
            print "n=%02d (%02d%%)" % (n, (n * 100) / n_max)

    del draw
    image.save(datetime.now().isoformat()+"_"+str(size[0])+"x"+str(size[1])+".png", 'png')
    image.show()

def calculateNumberSpiral():
    coordinate_function=coordinate_square
    # coordinate_function=coordinate_archimedes

    from PIL import Image, ImageDraw
    measure=8268
    size = (measure, measure)
    image = Image.new('RGB', size)
    center = (size[0] / 2, size[1] / 2)
    red = (255,0,0)
    spacing = 40

    draw = ImageDraw.Draw(image)
    # number spiral
    pos = center
    for n in range(1,100*100 + 1):
        c=coordinate_function(n)
        line_pos=(spacing*c[0]+center[0], spacing*c[1]+center[0])
        draw.line(pos+line_pos, fill=red)
        pos=line_pos

    for n in range(1,100*100 + 1):
        c=coordinate_function(n)
        text_pos=(spacing*c[0]+center[0], spacing*c[1]+center[0])
        text = str(n)
        draw.text(text_pos, text, fill=red)
    del draw

    image.show()

if __name__=='__main__':
    calculateDotImage()
    # calculateNumberSpiral()
