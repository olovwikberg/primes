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

def interpolateColor(backgroundColor=(0,0,0), color=(255,255,255), k=0.5):
    return (
        int(backgroundColor[0] + k * (color[0] - backgroundColor[0])),
        int(backgroundColor[1] + k * (color[1] - backgroundColor[1])),
        int(backgroundColor[2] + k * (color[2] - backgroundColor[2]))
        )

def dimColor(color=(255, 255, 255), k=0.5):
    return (
        int(k * color[0]),
        int(k * color[1]),
        int(k * color[2])
        )

def oldNewsPaperColors():
    color=(30, 30, 27)
    backgroundColor=(244, 244, 226)
    # edgeColor=interpolateColor(color, backgroundColor, 0.3)
    primeColor=(50, 10, 10)
    return color, backgroundColor, primeColor

def darkAndBlue():
    color=(117, 180, 224)
    backgroundColor=(52, 52, 52)
    # edgeColor=interpolateColor(color, backgroundColor, 0.3)
    primeColor=(color[2], color[1], color[0])
    return color, backgroundColor, primeColor

def drawOutlinedText(draw=None, pos=None, text=None, fill=None, outline=None):
    draw.text((pos[0]-1, pos[1]-1), text, fill=outline)
    draw.text((pos[0]-0, pos[1]-1), text, fill=outline)
    draw.text((pos[0]+1, pos[1]-1), text, fill=outline)
    draw.text((pos[0]+1, pos[1]-0), text, fill=outline)
    draw.text((pos[0]+1, pos[1]+1), text, fill=outline)
    draw.text((pos[0]-0, pos[1]+1), text, fill=outline)
    draw.text((pos[0]-1, pos[1]+1), text, fill=outline)
    draw.text((pos[0]-1, pos[1]-0), text, fill=outline)

    draw.text((pos[0]  , pos[1]  ), text, fill=fill)

d={}

def calculateDotImage(
    size=None, 
    scale=None,
    spacing=None, 
    colorSet=None, 
    doDimColors=False, 
    coordinate_function=coordinate_archimedes, 
    withCircles=True, 
    fillPrimes=True, 
    fillNonPrimes=True, 
    labelPrimes=False, 
    labelNonPrimes=False, 
    doMarkPrimes=False
    ):
    from PIL import Image, ImageDraw
    
    # Set dynamic default values
    if size == None:
        size = (2000, 2000)
    if scale == None:
        scale = 7
    if spacing == None:
        spacing = 3
    if colorSet == None:
        color, backgroundColor, primeColor=darkAndBlue()
    else:
        color, backgroundColor, primeColor=colorSet
    if not doDimColors:
        dimmedColor = color
        dimmedPrimeColor = primeColor

    if not doMarkPrimes:
        primeColor = color
        dimmedPrimeColor = color

    image = Image.new('RGB', size)
    center = (size[0] / 2, size[1] / 2)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0) + size, fill=backgroundColor)
    n_max = int(0.9 * max(size[0], size[1]) * max(size[0], size[1]) / (scale * scale * spacing * spacing))

    # draw one centimeter red line in center (at 300 ppi)
    # draw.line((center[0], center[1], center[0]+int(300/2.54), center[1]), fill=255)

    print "Crunching numbers (creating integer list and calculating number of factors for each integer)..."
    integer_list = range(1, n_max+1)
    number_of_factors_list = [ len(factors(n)) for n in integer_list ]
    print "done!"

    if doDimColors:
        print "Dim is on, sorting integer list on number of factors..."
        number_of_factors_list, integer_list = zip(*sorted(zip(number_of_factors_list, integer_list)))
        print "done!"

    print "Drawing..."
    for len_factors, n in zip(number_of_factors_list, integer_list):
        c=coordinate_function(n)
        pos=(scale*spacing*c[0]+center[0], scale*spacing*c[1]+center[1])

        scale_len_factors = scale * math.sqrt(len_factors)
        ellipse_poss=(pos[0] - scale_len_factors / 2, pos[1] - scale_len_factors / 2, pos[0] + scale_len_factors / 2, pos[1] + scale_len_factors / 2)

        # 1 is a prime in this program :)
        isPrime=len_factors<=2

        if isPrime and labelPrimes or not isPrime and labelNonPrimes:
            text = str(n)
            textsize=draw.textsize(text)


        if doDimColors:
            max_len_factors = 40
            max_scale_len_factors = scale * math.sqrt(max_len_factors-2)
            k = min(max(
                (scale_len_factors-4) / max_scale_len_factors
                , 0), 1)

            if isPrime:
                dimmedPrimeColor=interpolateColor(backgroundColor=backgroundColor, color=primeColor, k=k)
            else:
                dimmedColor=interpolateColor(backgroundColor=backgroundColor, color=color, k=k)

        if withCircles:
            if isPrime:
                if fillPrimes:
                    draw.ellipse(ellipse_poss, fill=dimmedPrimeColor)
                else:
                    draw.ellipse(ellipse_poss, outline=dimmedPrimeColor)
            else:
                if fillNonPrimes:
                    draw.ellipse(ellipse_poss, fill=dimmedColor)
                else:
                    draw.ellipse(ellipse_poss, outline=dimmedColor)

        if isPrime and labelPrimes:
            if fillPrimes:
                drawOutlinedText(
                    draw=draw, 
                    pos=(pos[0] - textsize[0]/2, pos[1] - textsize[1]/2), 
                    text=text, 
                    fill=backgroundColor, 
                    outline=dimmedPrimeColor
                    )
            else:
                draw.text((pos[0]-textsize[0]/2, pos[1]-textsize[1]/2), text, fill=dimmedPrimeColor)

        if not isPrime and labelNonPrimes:
            if fillNonPrimes:
                drawOutlinedText(
                    draw=draw, 
                    pos=(pos[0] - textsize[0]/2, pos[1] - textsize[1]/2), 
                    text=text, 
                    fill=backgroundColor, 
                    outline=dimmedColor
                    )
            else:
                draw.text((pos[0]-textsize[0]/2, pos[1]-textsize[1]/2), text, fill=dimmedColor)

        # if n % 1000 == 0:
        #     print "n=%02d (%02d%%)" % (n, (n * 100) / n_max)

    print "done!"
    del draw

    return image

if __name__=='__main__':
    # size=(2000, 1000)
    # size=(2000, 2000)
    size=(8268, 5906)
    # size=(8268, 8268)

    image = calculateDotImage(size=size)
    # image = calculateDotImage(size=size, colorSet=oldNewsPaperColors(), doDimColors=True)

    # image = calculateDotImage(
    #     size=size,

    #     # scale=12,
    #     scale=7,

    #     spacing=3,

    #     colorSet=darkAndBlue(),
    #     # colorSet=oldNewsPaperColors()

    #     # coordinate_function=coordinate_square, 
    #     coordinate_function=coordinate_archimedes, 

    #     withCircles=True, 

    #     fillPrimes=True,
    #     fillNonPrimes=True,

    #     labelPrimes=False, 
    #     labelNonPrimes=False, 

    #     doMarkPrimes=False
    #     )

    image.show()

    doneSaving = False
    while not doneSaving:
        try:
            doneSaving=False
            ans=raw_input("Save image? [Y/N] ")
            if ans=="y" or ans=="Y":
                fileName = datetime.now().isoformat()+"_"+str(size[0])+"x"+str(size[1])+".png"
                print "Saving image as: " + fileName
                image.save(fileName, 'png')
                doneSaving=True
            elif ans=="n" or ans=="N":
                doneSaving=True
        except:
            pass
    print "Done!"
