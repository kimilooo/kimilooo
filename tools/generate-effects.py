"""Original GitHub motion graphics. Never edits the AI-generated poster.
Requires Pillow and NumPy. Set PROFILE_FONT_DIR for a custom DejaVu directory.
"""
from pathlib import Path
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / 'assets'
OUT.mkdir(exist_ok=True)
FONT_DIR = Path(os.environ.get('PROFILE_FONT_DIR', '/usr/share/fonts/truetype/dejavu'))
W = 900
PINK, PEARL, MUTED = '#efadc0', '#f9e9ed', '#b990a4'

def font(size, serif=False, mono=False):
    name = 'DejaVuSansMono.ttf' if mono else 'DejaVuSerif.ttf' if serif else 'DejaVuSans.ttf'
    return ImageFont.truetype(str(FONT_DIR / name), size)

def centered(draw, xy, text, size, fill=PEARL, serif=False, mono=False):
    face = font(size, serif, mono)
    box = draw.textbbox((0, 0), text, font=face)
    draw.text((xy[0]-(box[2]-box[0])/2, xy[1]), text, font=face, fill=fill)

def background(height):
    yy, xx = np.mgrid[:height, :W]
    glow = np.exp(-((xx-W*.18)/(W*.55))**2-((yy-height*.5)/(height*1.4))**2)
    rgb = np.zeros((height, W, 3), dtype=np.uint8)
    for i, (base, lift) in enumerate([(17, 20), (12, 6), (22, 14)]):
        rgb[:, :, i] = base + glow*lift
    return Image.fromarray(rgb)

def star(draw, x, y, size, color):
    draw.polygon([(x,y-size),(x+size*.23,y-size*.23),(x+size,y),
                  (x+size*.23,y+size*.23),(x,y+size),(x-size*.23,y+size*.23),
                  (x-size,y),(x-size*.23,y-size*.23)], fill=color)

def petal(draw, x, y, size, angle, color):
    points=[]
    for j in range(24):
        theta=2*math.pi*j/24
        px=math.cos(theta)*size*.5
        py=math.sin(theta)*size*(.78+.17*math.cos(theta))
        points.append((x+px*math.cos(angle)-py*math.sin(angle),
                       y+px*math.sin(angle)+py*math.cos(angle)))
    draw.polygon(points, fill=color)

def petals(image, t, count=16):
    draw=ImageDraw.Draw(image);rng=random.Random(21)
    for i in range(count):
        x=rng.uniform(-20,W+20);y=rng.uniform(0,image.height)
        size=rng.uniform(3,7);speed=rng.choice([1,2]);phase=rng.uniform(0,math.tau)
        x=(x+28*math.sin(math.tau*t+phase))%W
        y=(y+t*image.height*speed)%image.height
        petal(draw,x,y,size,phase+math.tau*t,rng.choice(['#e1a0b7','#c681a0','#f2c5d2']))
    for i in range(7):
        pulse=.5+.5*math.sin(math.tau*t+i)
        star(draw,78+i*125,12+(i%3)*9,1+2*pulse,'#b4869e')

def film_edge(draw,height,t):
    for y in [7,height-15]:
        for x in range(-22,W+22,29):
            x=x+int(29*t)
            draw.rounded_rectangle((x,y,x+11,y+6),2,fill='#795164')
    draw.line((20,23,W-20,23),fill='#5b394b')
    draw.line((20,height-24,W-20,height-24),fill='#5b394b')

def save_motion(name,frames,duration=100):
    frames[0].save(OUT/(name+'-still.png'),optimize=True)
    palette=frames[0].quantize(colors=128)
    indexed=[frame.quantize(palette=palette,dither=Image.Dither.NONE) for frame in frames]
    indexed[0].save(OUT/(name+'.gif'),save_all=True,append_images=indexed[1:],
                    duration=duration,loop=0,optimize=True,disposal=1)

def intro():
    height=168;base=background(height);frames=[]
    for n in range(60):
        t=n/60;image=base.copy();draw=ImageDraw.Draw(image)
        film_edge(draw,height,t);petals(image,t,13)
        draw.rounded_rectangle((30,35,131,132),16,fill='#211420',outline='#9e657f',width=1)
        draw.ellipse((42,45,119,122),outline='#664251',width=1)
        draw.arc((42,45,119,122),-90,-90+t*360,fill=PINK,width=2)
        centered(draw,(80,55),['3','2','1','K','K','K'][n//10],40,serif=True)
        centered(draw,(513,35),'A KIMILOO ORIGINAL',12,fill=MUTED,mono=True)
        centered(draw,(513,59),"Welcome to my little cinema.",31,serif=True)
        centered(draw,(513,105),'ADMIT ONE  /  SOFT PETALS. SHARP IDEAS.',12,fill=PINK,mono=True)
        frames.append(image)
    save_motion('cinema-intro',frames)

def roles():
    height=90;base=background(height);frames=[]
    labels=['AI filmmaker.','Creative builder.','Web3 storyteller.']
    for n in range(120):
        t=n/120;image=base.copy();draw=ImageDraw.Draw(image);petals(image,t,8)
        label=labels[n//40];phase=n%40;length=min(len(label),phase//2+1)
        visible=label if n==0 else label[:length]
        centered(draw,(450,23),visible,28,fill=PEARL,serif=True)
        width=draw.textlength(visible,font=font(28,serif=True));cursor=450+width/2+8
        if phase%12<8:draw.line((cursor,28,cursor,55),fill=PINK,width=2)
        draw.line((150,78,750,78),fill='#5d394d');star(draw,450,78,5,PINK)
        frames.append(image)
    save_motion('casting',frames)

def outro():
    height=118;base=background(height);frames=[]
    for n in range(60):
        t=n/60;image=base.copy();draw=ImageDraw.Draw(image);petals(image,t,20)
        draw.rounded_rectangle((20,10,W-21,height-11),16,outline='#5e3a50',width=1)
        centered(draw,(450,24),'Meet me where the ideas bloom.',24,serif=True)
        centered(draw,(450,66),'MADE WITH CURIOSITY, CODE & A LITTLE DRAMA.',11,fill=MUTED,mono=True)
        frames.append(image)
    save_motion('end-credits',frames)

def svg_card(name,eyebrow,title,description,footer,accent='#efadc0'):
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="224" viewBox="0 0 900 224" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">{description}</desc>
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#291827"/><stop offset="1" stop-color="#120e19"/></linearGradient></defs>
<rect x="1" y="1" width="898" height="222" rx="18" fill="url(#bg)" stroke="#674258"/>
<path d="M734 1 Q804 92 899 117 M761 1 Q819 48 897 64" fill="none" stroke="#855568" stroke-width="2"/>
<g fill="{accent}" opacity=".6"><ellipse cx="786" cy="55" rx="7" ry="15" transform="rotate(35 786 55)"/><ellipse cx="833" cy="84" rx="5" ry="11" transform="rotate(-26 833 84)"/><ellipse cx="865" cy="48" rx="4" ry="10"/></g>
<text x="34" y="37" fill="#b990a4" font-family="monospace" font-size="12" letter-spacing="3">{eyebrow}</text>
<text x="34" y="89" fill="#fae7ee" font-family="Georgia,serif" font-size="38">{title}</text>
<text x="34" y="126" fill="#d1aebf" font-family="Arial,sans-serif" font-size="17">{description}</text>
<path d="M34 155 H865" stroke="#513547"/>
<text x="34" y="190" fill="{accent}" font-family="monospace" font-size="12" letter-spacing="1.3">{footer}</text>
<path d="M821 188 H851 M841 178 L851 188 L841 198" stroke="{accent}" stroke-width="2" fill="none"/>
</svg>'''
    (OUT/(name+'.svg')).write_text(svg)

def button(name,label,subtitle):
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="280" height="72" viewBox="0 0 280 72" role="img" aria-label="{label}">
<rect x="1" y="1" width="278" height="70" rx="14" fill="#211421" stroke="#8a5671"/>
<path d="M21 36 L25 29 L29 36 L25 43Z" fill="#edb1c8"/>
<text x="43" y="30" fill="#f9e9ed" font-family="Arial,sans-serif" font-size="16">{label}</text>
<text x="43" y="51" fill="#ba92a8" font-family="monospace" font-size="10" letter-spacing="1">{subtitle}</text>
<path d="M245 28 L253 36 L245 44" fill="none" stroke="#edb1c8" stroke-width="1.5"/>
</svg>'''
    (OUT/(name+'.svg')).write_text(svg)

if __name__=='__main__':
    intro();roles();outro()
    svg_card('paybox-lens','NOW SHOWING / FEATURE 01','PayBox Lens','Your wallet activity, in focus.','LOCAL SQLITE / PRIVACY / OPEN SOURCE')
    svg_card('electonet','DOUBLE FEATURE / FEATURE 02','Electonet','A modern dashboard for server monitoring.','MONITORING / MATRIX / SSH','#cbb7ed')
    button('link-x','Say hi on X','@KIMILOOWEB3')
    button('link-work','Browse my projects','OPEN-SOURCE EXPERIMENTS')
    button('link-lens','Enter PayBox Lens','BUILT BY KIMILOO')
    print('Rendered 3 looping GIFs, 3 stills and 5 SVG graphics.')
