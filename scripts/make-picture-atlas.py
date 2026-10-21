"""Build local word illustrations; Noto Emoji (OFL) plus original vector drawings."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, re, math, os
ROOT=Path(__file__).resolve().parents[1]
words=re.search(r'`\n(.*?)\n`', (ROOT/'src/words.ts').read_text(),re.S)[1].splitlines()
emoji={}
for line in '''
Elephant 🐘
Pizza 🍕
Dinosaur 🦕
Volcano 🌋
Helicopter 🚁
Penguin 🐧
Toothbrush 🪥
Castle 🏰
Watermelon 🍉
Telescope 🔭
Giraffe 🦒
Lion 🦁
Zebra 🦓
Kangaroo 🦘
Koala 🐨
Panda 🐼
Tiger 🐅
Dolphin 🐬
Whale 🐋
Shark 🦈
Octopus 🐙
Jellyfish 🪼
Crab 🦀
Lobster 🦞
Turtle 🐢
Crocodile 🐊
Snake 🐍
Lizard 🦎
Frog 🐸
Butterfly 🦋
Bee 🐝
Ant 🐜
Spider 🕷
Ladybug 🐞
Snail 🐌
Owl 🦉
Eagle 🦅
Parrot 🦜
Flamingo 🦩
Peacock 🦚
Swan 🦢
Duck 🦆
Chicken 🐔
Rooster 🐓
Turkey 🦃
Camel 🐪
Horse 🐎
Donkey 🫏
Goat 🐐
Sheep 🐑
Cow 🐄
Pig 🐖
Rabbit 🐇
Squirrel 🐿
Hedgehog 🦔
Fox 🦊
Wolf 🐺
Bear 🐻
Deer 🦌
Moose 🫎
Raccoon 🦝
Skunk 🦨
Bat 🦇
Otter 🦦
Seal 🦭
Bison 🦬
Rhino 🦏
Hippo 🦛
Gorilla 🦍
Chimpanzee 🐒
Cheetah 🐆
Sloth 🦥
Apple 🍎
Banana 🍌
Orange 🍊
Lemon 🍋
Strawberry 🍓
Blueberry 🫐
Grape 🍇
Pineapple 🍍
Mango 🥭
Peach 🍑
Pear 🍐
Cherry 🍒
Coconut 🥥
Avocado 🥑
Tomato 🍅
Potato 🥔
Carrot 🥕
Broccoli 🥦
Spinach 🥬
Onion 🧅
Garlic 🧄
Mushroom 🍄
Pumpkin 🎃
Cucumber 🥒
Corn 🌽
Peas 🫛
Rice 🍚
Pasta 🍝
Bread 🍞
Croissant 🥐
Bagel 🥯
Pancake 🥞
Waffle 🧇
Cereal 🥣
Egg 🥚
Cheese 🧀
Butter 🧈
Icecream 🍨
Chocolate 🍫
Cookie 🍪
Cake 🎂
Cupcake 🧁
Donut 🍩
Popcorn 🍿
Pretzel 🥨
Hamburger 🍔
Sandwich 🥪
Taco 🌮
Burrito 🌯
Sushi 🍣
Soup 🍲
Salad 🥗
Curry 🍛
Noodles 🍜
Dumpling 🥟
Coffee ☕
Tea 🍵
Honey 🍯
Salt 🧂
Ginger 🫚
Rose 🌹
Tulip 🌷
Sunflower 🌻
Cactus 🌵
Bamboo 🎋
Oak 🌳
Palm 🌴
Fern 🌿
Daisy 🌼
Mountain 🏔
Ocean 🌊
Desert 🏜
Island 🏝
Beach 🏖
Rainbow 🌈
Thunder ⛈
Lightning 🌩
Snowflake ❄
Blizzard 🌨
Fog 🌫
Tornado 🌪
Sunrise 🌅
Sunset 🌇
Moon 🌙
Star ⭐
Comet ☄
Planet 🪐
Galaxy 🌌
Meteor 🌠
Astronaut 🧑‍🚀
Rocket 🚀
Satellite 🛰
Sailboat ⛵
Canoe 🛶
Ferry ⛴
Train 🚆
Bicycle 🚲
Motorcycle 🏍
Scooter 🛵
Bus 🚌
Airplane ✈
Ambulance 🚑
Tractor 🚜
Firetruck 🚒
Skateboard 🛹
Rollerskates 🛼
Umbrella ☂
Backpack 🎒
Suitcase 🧳
Key 🔑
Lock 🔒
Mirror 🪞
Clock 🕒
Calendar 📅
Candle 🕯
Lantern 🏮
Flashlight 🔦
Ladder 🪜
Scissors ✂
Hammer 🔨
Screwdriver 🪛
Paintbrush 🖌
Pencil ✏
Notebook 📓
Envelope ✉
Compass 🧭
Map 🗺
Microscope 🔬
Camera 📷
Microphone 🎤
Headphones 🎧
Piano 🎹
Guitar 🎸
Violin 🎻
Drum 🥁
Trumpet 🎺
Flute 🪈
Accordion 🪗
Chess ♟
Dice 🎲
Puzzle 🧩
Kite 🪁
Yo-yo 🪀
Frisbee 🥏
Football 🏈
Basketball 🏀
Tennis 🎾
Bowling 🎳
Golf ⛳
Hockey 🏒
Surfboard 🏄
Snowboard 🏂
Parachute 🪂
Carousel 🎠
Ferriswheel 🎡
Library 📚
Museum 🏛
Hospital 🏥
School 🏫
Theater 🎭
Airport 🛫
Bridge 🌉
Elevator 🛗
Fountain ⛲
Statue 🗽
Tent ⛺
Cabin 🏡
'''.strip().splitlines():
 word,glyph=line.split(' ',1);emoji[word.upper()]=glyph

# Original compact vector pictures for subjects without an exact emoji.
S={}
def add(names,svg):
 for n in names.split(','):S[n.upper()]=svg
add('Seahorse','<path d="M72 25 Q104 12 104 36 L85 43 Q76 54 91 65 Q102 91 78 104 Q47 112 49 91 Q53 77 66 88" fill="none" stroke="#f59e0b" stroke-width="15" stroke-linecap="round"/><path d="M78 43L57 64L83 61" fill="#ffcf75"/><circle cx="89" cy="25" r="3"/>')
add('Dragonfly','<ellipse cx="42" cy="45" rx="33" ry="12" fill="#83e6ed" transform="rotate(25 42 45)"/><ellipse cx="85" cy="45" rx="33" ry="12" fill="#83e6ed" transform="rotate(-25 85 45)"/><ellipse cx="42" cy="70" rx="30" ry="10" fill="#b4f5ec"/><ellipse cx="85" cy="70" rx="30" ry="10" fill="#b4f5ec"/><path d="M64 42V113" stroke="#246d7e" stroke-width="10"/><circle cx="64" cy="36" r="12" fill="#246d7e"/>')
add('Firefly','<ellipse cx="64" cy="78" rx="26" ry="34" fill="#ffe656"/><ellipse cx="47" cy="52" rx="18" ry="28" fill="#63868c" transform="rotate(-30 47 52)"/><ellipse cx="81" cy="52" rx="18" ry="28" fill="#63868c" transform="rotate(30 81 52)"/><circle cx="64" cy="29" r="13" fill="#233747"/><path d="M23 88L9 94M105 88L119 94M64 116V125" stroke="#ffe656" stroke-width="4"/>')
add('Ostrich','<ellipse cx="58" cy="63" rx="34" ry="24" fill="#344356"/><path d="M79 57L91 21M46 83L41 113M65 84L70 113" stroke="#e9bfa8" stroke-width="9"/><circle cx="92" cy="20" r="12" fill="#e9bfa8"/><path d="M103 18L121 22L103 26" fill="#ef9b37"/><circle cx="94" cy="17" r="2"/>')
add('Walrus','<ellipse cx="64" cy="77" rx="48" ry="31" fill="#a97252"/><circle cx="72" cy="46" r="28" fill="#b37c5a"/><path d="M57 56L58 88L65 59M78 59L87 87L86 53" fill="#fff8df"/><circle cx="64" cy="38" r="3"/><circle cx="82" cy="38" r="3"/><ellipse cx="73" cy="48" rx="8" ry="5" fill="#543e38"/>')
add('Lemur','<path d="M79 91 Q116 85 108 36 Q105 7 91 16" fill="none" stroke="#788692" stroke-width="16"/><path d="M105 43L114 43M101 22L111 23M99 65L114 65" stroke="#263343" stroke-width="9"/><ellipse cx="54" cy="80" rx="26" ry="32" fill="#aab7c4"/><path d="M31 35L27 11L49 29M68 28L84 11L79 39" fill="#8f9dac"/><circle cx="55" cy="43" r="27" fill="#c9d0d6"/><ellipse cx="43" cy="43" rx="10" ry="13" fill="#303340"/><ellipse cx="68" cy="43" rx="10" ry="13" fill="#303340"/><circle cx="43" cy="43" r="4" fill="#ffc95c"/><circle cx="68" cy="43" r="4" fill="#ffc95c"/>')
add('Meerkat','<ellipse cx="64" cy="78" rx="23" ry="40" fill="#c58d56"/><ellipse cx="65" cy="84" rx="14" ry="27" fill="#efd0a1"/><circle cx="64" cy="35" r="25" fill="#c58d56"/><ellipse cx="51" cy="33" rx="8" ry="6" fill="#4b3932"/><ellipse cx="77" cy="33" rx="8" ry="6" fill="#4b3932"/><circle cx="64" cy="44" r="5" fill="#3c302a"/>')
add('Platypus','<ellipse cx="64" cy="73" rx="40" ry="25" fill="#8d6247"/><ellipse cx="23" cy="68" rx="16" ry="28" fill="#73503b" transform="rotate(-32 23 68)"/><ellipse cx="98" cy="76" rx="24" ry="12" fill="#d7a253"/><circle cx="84" cy="58" r="4"/>')
add('Lime','<ellipse cx="64" cy="64" rx="43" ry="34" fill="#70bf33" transform="rotate(-30 64 64)"/><path d="M38 48Q63 30 82 42" fill="none" stroke="#bcec7d" stroke-width="6" stroke-linecap="round"/>')
add('Raspberry','<path d="M40 26L63 40L89 26L76 48H50Z" fill="#49a778"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="13" fill="#e34d87" stroke="#a82761" stroke-width="2"/>' for x,y in [(48,52),(74,52),(35,72),(61,72),(87,72),(48,92),(74,92),(61,109)]))
add('Yogurt,Oatmeal','<path d="M20 55H108Q102 113 64 113Q27 113 20 55" fill="#69bace"/><ellipse cx="64" cy="55" rx="44" ry="13" fill="#fff2da"/><path d="M84 51L108 13" stroke="#9aa6b8" stroke-width="8" stroke-linecap="round"/>')
add('Lemonade,Milkshake','<path d="M36 39H94L86 112H44Z" fill="#ffd76f" stroke="#fcf5d8" stroke-width="4"/><path d="M77 87L87 14H108" stroke="#d65f83" stroke-width="7" fill="none"/><circle cx="40" cy="40" r="18" fill="#ffe383" stroke="#fff2ac" stroke-width="5"/>')
add('Jam','<rect x="31" y="37" width="66" height="76" rx="15" fill="#cc4163"/><rect x="28" y="20" width="72" height="24" rx="5" fill="#e8bc80"/><rect x="38" y="59" width="52" height="32" rx="6" fill="#fff0d8"/><ellipse cx="64" cy="74" rx="11" ry="13" fill="#dd375c"/>')
add('Mustard,Ketchup','<path d="M48 26L53 7H73L78 26V40Q99 44 99 62V112H29V62Q29 44 48 40Z" fill="#efb634"/><rect x="40" y="64" width="48" height="26" rx="5" fill="#fff3d8"/>')
add('Pepper','<path d="M44 43Q25 59 42 88L34 113H94L86 88Q103 59 84 43Z" fill="#a06d47"/><rect x="40" y="24" width="48" height="23" rx="8" fill="#bb895e"/><path d="M62 23V11H77" stroke="#c6d0db" stroke-width="7"/>')
add('Cinnamon','<path d="M22 91L85 24L109 43L46 110Z" fill="#ad6840"/><path d="M36 97L96 36M49 108L108 46" stroke="#e2aa6d" stroke-width="5"/><ellipse cx="97" cy="32" rx="17" ry="10" fill="#77472d" transform="rotate(40 97 32)"/>')
add('Vanilla','<path d="M27 110Q71 79 88 16M37 113Q87 73 99 22" stroke="#584130" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M49 34Q18 4 20 40Q0 57 35 61Q33 95 54 67Q88 77 70 48Q91 16 60 29Z" fill="#fff0b7"/><circle cx="49" cy="49" r="12" fill="#ffcb52"/>')
add('Basil,Rosemary,Lavender,Moss','<path d="M38 117L78 15" stroke="#41885d" stroke-width="5"/>'+''.join(f'<ellipse cx="{x}" cy="{y}" rx="18" ry="8" fill="#63b57f" transform="rotate({a} {x} {y})"/>' for x,y,a in [(47,88,30),(69,76,-25),(59,59,30),(82,48,-25),(70,30,30)]))
add('Willow','<rect x="58" y="60" width="12" height="56" fill="#8f684b"/><path d="M12 77Q8 10 64 9Q122 11 115 77L102 48L96 95L82 46L72 86L60 42L44 91L39 46L25 93Z" fill="#70ad70"/>')
add('Orchid','<path d="M60 119L65 47" stroke="#4c9a65" stroke-width="5"/><path d="M64 50Q30 1 24 37Q3 58 48 67Q47 101 65 73Q92 104 88 69Q131 57 102 39Q99 0 64 50" fill="#d597dc"/><circle cx="64" cy="58" r="11" fill="#f8d96b"/>')
add('Pinecone','<path d="M64 12Q22 23 32 85Q36 111 64 119Q96 107 98 77Q102 28 64 12" fill="#a4774d"/>'+''.join(f'<path d="M{x-16} {y}L{x} {y+12}L{x+16} {y}" fill="none" stroke="#d4a87a" stroke-width="5"/>' for x,y in [(64,30),(49,48),(79,48),(64,67),(51,85),(77,85)]))
add('Acorn','<path d="M36 57H94Q90 106 64 114Q40 105 36 57" fill="#c78c4c"/><path d="M27 58Q28 24 64 25Q101 25 103 58Z" fill="#825a3b"/><path d="M64 27L72 10" stroke="#825a3b" stroke-width="9"/>')
add('River,Lake,Waterfall,Glacier,Canyon,Valley,Meadow,Cliff,Forest,Cave,Dew,Hail,Earthquake,Avalanche','')
# Hand-drawn landscapes use distinct silhouettes.
S['RIVER']='<path d="M46 9H91Q28 48 75 68Q112 92 55 125H9Q82 89 45 70Q0 48 46 9" fill="#61bce4"/>'
S['LAKE']='<ellipse cx="64" cy="82" rx="57" ry="29" fill="#61bce4"/><path d="M9 58L35 15L58 58M63 53L91 8L120 60" fill="#77a387"/><path d="M31 83H74M63 95H100" stroke="#c2effa" stroke-width="4"/>'
S['WATERFALL']='<path d="M8 17H121V113H8Z" fill="#849d8f"/><path d="M41 18H86L92 100H35Z" fill="#8cdbf4"/><path d="M51 30L48 89M70 26L76 88" stroke="#e3f9ff" stroke-width="7"/><ellipse cx="64" cy="106" rx="55" ry="13" fill="#8cdbf4"/>'
S['GLACIER']='<path d="M7 105L23 40L44 58L67 13L89 54L108 34L122 105Z" fill="#9bdeeb"/><path d="M67 13L57 91L89 54M23 40L36 101M108 34L98 98" fill="none" stroke="#e3fbff" stroke-width="6"/>'
S['CANYON']='<path d="M6 17L46 28L53 107H5ZM83 28L123 12V111H73Z" fill="#c27650"/><path d="M8 48L47 59M81 58L121 42M8 77L50 88M78 91L121 76" stroke="#e4ab73" stroke-width="8"/>'
S['VALLEY']='<path d="M2 21L65 103L124 14V117H2Z" fill="#7ab17e"/><path d="M6 21L40 24L65 103M124 14L93 30L65 103" fill="#90b8a5"/>'
S['MEADOW']='<path d="M5 83Q48 54 124 79V116H5Z" fill="#73b97c"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="{c}"/>' for x,y,c in [(23,89,'#ffe28b'),(49,101,'#d8b9ec'),(88,89,'#ffe28b'),(110,103,'#e8a4c3')])
S['CLIFF']='<path d="M5 23H77L87 47L62 58L68 88L54 118H5Z" fill="#a18469"/><path d="M5 23H77" stroke="#72b279" stroke-width="12"/><path d="M74 111H123" stroke="#7abfdf" stroke-width="12"/>'
S['FOREST']=''.join(f'<rect x="{x-4}" y="67" width="8" height="48" fill="#7b6550"/><path d="M{x} {y}L{x-25} 87H{x+25}Z" fill="{c}"/>' for x,y,c in [(28,27,'#63ac81'),(98,26,'#63ac81'),(64,6,'#32836b')])
S['CAVE']='<path d="M4 115L17 45L48 12L94 26L121 115Z" fill="#9a9ba6"/><path d="M31 115V79Q31 46 65 46Q99 46 99 79V115Z" fill="#333848"/>'
S['DEW']='<ellipse cx="64" cy="77" rx="52" ry="27" fill="#6bb281" transform="rotate(-25 64 77)"/><path d="M64 20Q35 60 64 67Q94 60 64 20" fill="#9cdef5"/>'
S['HAIL']='<path d="M20 49Q7 25 36 22Q60 2 81 23Q115 16 116 48Z" fill="#b1c4d8"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="7" fill="#a8e0f5"/>' for x,y in [(24,80),(65,69),(96,92),(51,111)] )
S['EARTHQUAKE']='<path d="M7 68H121V114H7Z" fill="#ad8669"/><path d="M65 53L49 75L74 85L58 103L69 123" stroke="#423f47" stroke-width="8" fill="none"/><path d="M14 51L36 33L56 51V66H14Z" fill="#d39c7c"/>'
S['AVALANCHE']='<path d="M4 116L67 12L123 116Z" fill="#91a6b8"/><path d="M67 12L35 64L64 55L82 78L93 59Z" fill="#fff7ed"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e5f5fa"/>' for x,y,r in [(61,62,12),(72,78,16),(57,99,22),(86,105,18)] )
add('Submarine','<ellipse cx="64" cy="77" rx="52" ry="26" fill="#f2bf57"/><path d="M60 53V32H80" stroke="#cf9650" stroke-width="11" fill="none"/>'+''.join(f'<circle cx="{x}" cy="76" r="9" fill="#4c8cb1" stroke="#fff2c4" stroke-width="4"/>' for x in [36,63,90]))
add('Bulldozer','<rect x="12" y="83" width="82" height="24" rx="12" fill="#485567"/><rect x="22" y="59" width="72" height="27" fill="#f3bb46"/><path d="M43 59V25H78V59" fill="#93d0e6" stroke="#e5a537" stroke-width="8"/><path d="M100 57L116 51V105H98Z" fill="#d39435"/>')
add('Hotairballoon','<path d="M64 7C1 7 7 72 49 88H79C120 72 126 7 64 7" fill="#e98084"/><path d="M64 7C32 7 33 67 54 87H73C97 62 95 7 64 7" fill="#f8d484"/><path d="M49 85L53 105M79 85L75 105" stroke="#806952" stroke-width="4"/><rect x="48" y="104" width="33" height="19" rx="4" fill="#a7794e"/>')
add('Wallet','<rect x="15" y="34" width="100" height="69" rx="12" fill="#a67350" stroke="#d9a878" stroke-width="5"/><rect x="78" y="53" width="42" height="32" rx="8" fill="#c9966b"/><circle cx="95" cy="69" r="5" fill="#efd9ab"/>')
add('Pillow,Blanket','<path d="M16 28Q62 37 112 28Q105 66 112 103Q62 94 16 103Q23 66 16 28" fill="#b5b3ec" stroke="#e4def8" stroke-width="6"/>')
add('Hammock','<path d="M12 20L21 116M115 20L108 116" stroke="#956c51" stroke-width="8"/><path d="M15 38Q66 111 113 38Q67 133 15 38" fill="#e4a478"/><path d="M31 58L78 87M50 78L97 59" stroke="#fbe0ab" stroke-width="4"/>')
add('Eraser','<path d="M14 78L58 28L114 68L74 114H49Z" fill="#ed9eb9"/><path d="M14 78L39 50L92 91L74 114H49Z" fill="#b6d7e8"/><path d="M50 114H114" stroke="#d4e2ec" stroke-width="4"/>')
add('Stamp','<path d="M15 15H113V113H15Z" fill="#fff1da" stroke="#b4c1d0" stroke-width="5" stroke-dasharray="5 8"/><rect x="30" y="30" width="68" height="68" fill="#8ab8d7"/><path d="M32 92L59 51L75 72L88 59L98 92Z" fill="#537d86"/>')
add('Binoculars','<path d="M18 40H49L58 105H6ZM79 40H110L122 105H70Z" fill="#455265"/><path d="M43 65H85" stroke="#455265" stroke-width="18"/><circle cx="32" cy="96" r="23" fill="#88c8dd" stroke="#344052" stroke-width="9"/><circle cx="96" cy="96" r="23" fill="#88c8dd" stroke="#344052" stroke-width="9"/>')
add('Domino','<rect x="34" y="9" width="60" height="110" rx="10" fill="#f8ecd8" stroke="#797a89" stroke-width="5"/><path d="M39 64H89" stroke="#797a89" stroke-width="4"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="#414453"/>' for x,y in [(49,28),(78,48),(49,83),(78,102)]))
add('Marble','<circle cx="64" cy="64" r="48" fill="#9fe3eb"/><path d="M35 27Q108 44 43 105Q96 102 109 66Q106 23 63 16" fill="#ed92b5"/><circle cx="43" cy="40" r="12" fill="#e9fbfc"/>')
add('Trampoline','<path d="M26 79L19 116M100 79L109 116M63 86V120" stroke="#9dabbc" stroke-width="7"/><ellipse cx="64" cy="72" rx="55" ry="24" fill="#62b4c7"/><ellipse cx="64" cy="70" rx="43" ry="15" fill="#374d65"/>')
add('Lighthouse','<path d="M42 109L49 42H79L87 109Z" fill="#f6e7d6"/><path d="M47 58H81L82 76H45Z" fill="#d46d75"/><rect x="45" y="25" width="39" height="22" fill="#ffe49a" stroke="#6c7686" stroke-width="5"/><path d="M37 24L64 7L91 24Z" fill="#c16c71"/><path d="M41 33L8 21V49ZM88 33L120 19V51Z" fill="#ffe7a3" opacity=".6"/>')
add('Tunnel','<path d="M6 117V61Q6 8 64 8Q122 8 122 61V117Z" fill="#91a2ad"/><path d="M27 117V65Q27 31 64 31Q102 31 102 65V117Z" fill="#3e4e64"/><path d="M50 117L63 69L78 117" fill="#7c92a0"/><path d="M64 92V112" stroke="#f3dc94" stroke-width="4"/>')
add('Staircase','<path d="M7 114V91H30V68H54V45H78V21H117V114Z" fill="#96a7c4"/><path d="M7 91H30V68H54V45H78V21H117" fill="none" stroke="#d7e3f0" stroke-width="7"/>')
add('Windmill','<path d="M40 117L51 54H77L89 117" fill="#e3c9a3"/><path d="M64 62L35 12L20 20L58 67L107 40L100 24L62 57L90 109L106 98L69 64L17 91L28 105Z" fill="#ba8762"/><circle cx="64" cy="63" r="10" fill="#e6d6ba"/>')
add('Pyramid','<path d="M5 113L65 13L123 113Z" fill="#e0b467"/><path d="M65 13L75 113H123Z" fill="#bd8b4c"/><path d="M30 73H72M19 92H73" stroke="#efcf91" stroke-width="4"/>')
add('Igloo','<path d="M10 107V79Q10 18 64 18Q119 18 119 79V107Z" fill="#c6e4f0" stroke="#a1cbdc" stroke-width="4"/><path d="M16 57H111M10 80H117M43 24V55M83 24V55M30 58V79M64 58V79M98 58V79" stroke="#91bbd1" stroke-width="3"/><path d="M46 108V86Q46 67 65 67Q84 67 84 86V108Z" fill="#51758f"/>')
add('Barn','<path d="M13 52L64 14L115 52V114H13Z" fill="#ca676f"/><path d="M5 54L64 10L123 54" fill="none" stroke="#f3debe" stroke-width="8"/><rect x="40" y="64" width="49" height="50" fill="#873e4e" stroke="#f3debe" stroke-width="5"/><path d="M42 66L88 112M87 66L41 112" stroke="#f3debe" stroke-width="5"/>')
add('Greenhouse','<path d="M12 50L64 13L116 50V115H12Z" fill="#c0e6dc" stroke="#739c8b" stroke-width="5"/><path d="M12 50H116M39 32V113M89 32V113M12 82H116M64 14V113" stroke="#739c8b" stroke-width="4"/><path d="M26 110V94M100 110V94" stroke="#458a66" stroke-width="6"/><ellipse cx="25" cy="91" rx="10" ry="15" fill="#66ab7b"/><ellipse cx="100" cy="91" rx="10" ry="15" fill="#66ab7b"/>')
# Adjust shared drawings to retain recognizable color differences.
S['KETCHUP']=S['KETCHUP'].replace('#efb634','#df6463')
S['MILKSHAKE']=S['MILKSHAKE'].replace('#ffd76f','#e7a2c4').replace('<circle cx="40" cy="40" r="18" fill="#ffe383" stroke="#fff2ac" stroke-width="5"/>','<path d="M38 38Q32 17 52 19Q65 2 76 20Q99 16 95 38Z" fill="#fff1e4"/>')
S['OATMEAL']=S['OATMEAL'].replace('#fff2da','#d8b48a')
S['BLANKET']=S['BLANKET'].replace('#b5b3ec','#e6b17c')+'<path d="M30 40V90M50 40V90M70 40V90M90 40V90M28 55H99M28 76H99" stroke="#f9dcaa" stroke-width="5"/>'
S['LAVENDER']=S['LAVENDER'].replace('#63b57f','#b18adb')
S['ROSEMARY']=S['ROSEMARY'].replace('rx="18" ry="8"','rx="20" ry="3"')
S['MOSS']='<path d="M8 101Q14 65 36 74Q53 37 73 68Q106 51 119 101Z" fill="#72a969"/><path d="M29 86L35 76M60 85L64 68M92 88L103 79" stroke="#aed18d" stroke-width="4"/>'

emoji.update(dict(line.split(' ',1) for line in """
SANTA 🎅
REINDEER 🦌
SNOWMAN ⛄
STOCKING 🧦
PRESENT 🎁
CHRISTMAS 🎄
HALLOWEEN 🎃
THANKSGIVING 🦃
EASTER 🥚
VALENTINE 💌
HANUKKAH 🕎
DIWALI 🪔
RAMADAN 🌙
COUNTDOWN ⏳
FIREWORKS 🎆
CONFETTI 🎊
BALLOON 🎈
BIRTHDAY 🎂
COSTUME 🎭
MASK 🎭
GHOST 👻
WITCH 🧙‍♀️
VAMPIRE 🧛
ZOMBIE 🧟
SKELETON 💀
CANDY 🍬
ELF 🧝
SLEIGH 🛷
HEART ❤️
CUPID 👼
BOUQUET 💐
RIBBON 🎀
BELL 🔔
FESTIVAL 🎪
PARADE 🥁
SHAMROCK ☘
MOONCAKE 🥮
MENORAH 🕎
DRAGON 🐉
""".strip().splitlines()))
add('Candycane','<path d="M45 114V39Q45 5 76 10Q108 12 99 44" fill="none" stroke="#fff3dd" stroke-width="19" stroke-linecap="round"/><path d="M35 89L54 97M35 63L54 71M39 31L57 42M68 3L67 22M90 15L77 30" stroke="#e86f7d" stroke-width="10"/>')
add('Gingerbread','<circle cx="64" cy="25" r="20" fill="#c18a50"/><path d="M50 49L19 39L11 55L43 69L33 111L51 118L65 84L79 118L97 109L85 69L116 55L108 39L77 49Z" fill="#c18a50"/><circle cx="58" cy="22" r="3" fill="#fff2dd"/><circle cx="72" cy="22" r="3" fill="#fff2dd"/><path d="M55 32Q65 40 75 32" fill="none" stroke="#fff2dd" stroke-width="3"/><circle cx="65" cy="61" r="4" fill="#da676f"/><circle cx="65" cy="75" r="4" fill="#da676f"/>')
add('Wreath','<circle cx="64" cy="65" r="39" fill="none" stroke="#56936e" stroke-width="24"/><path d="M64 22L35 6L32 34L64 27L94 36L91 6Z" fill="#df6b7c"/><circle cx="32" cy="65" r="6" fill="#e37e87"/><circle cx="79" cy="100" r="6" fill="#e37e87"/><circle cx="96" cy="58" r="6" fill="#e37e87"/>')
add('Ornament','<path d="M64 4V20" stroke="#c8ad72" stroke-width="5"/><rect x="49" y="18" width="30" height="17" rx="4" fill="#d3b775"/><circle cx="64" cy="75" r="43" fill="#da6c83"/><path d="M26 69Q63 93 102 69" fill="none" stroke="#f6cc9e" stroke-width="9"/>')
add('Chimney','<path d="M6 113L56 66L123 113Z" fill="#8d8d9c"/><path d="M69 21H103V98H69Z" fill="#b57361"/><path d="M64 17H108V32H64Z" fill="#d5977b"/><path d="M71 48H101M71 68H101" stroke="#e8b59a" stroke-width="4"/>')
add('Snowglobe','<circle cx="64" cy="56" r="47" fill="#badfe8"/><path d="M17 75Q65 60 110 75" fill="#f1f6f2"/><path d="M64 25L38 72H89Z" fill="#578a77"/><path d="M28 96H101L108 119H20Z" fill="#b18464"/><circle cx="36" cy="40" r="4" fill="#fff"/><circle cx="85" cy="50" r="4" fill="#fff"/>')
add('Dreidel','<path d="M63 7V30" stroke="#bc9459" stroke-width="12"/><path d="M31 32H97V82L64 119L31 82Z" fill="#8bade0"/><path d="M64 34V116L97 82V34" fill="#648ec5"/><path d="M41 47H54V70H41" fill="none" stroke="#f1d68b" stroke-width="5"/>')
add('Kwanzaa','<path d="M17 108H111M64 61V108M32 79V99H96V79" fill="none" stroke="#b18050" stroke-width="9"/>'+''.join(f'<rect x="{x}" y="{y}" width="11" height="45" fill="{c}"/><path d="M{x+5} {y-17}Q{x-3} {y-5} {x+5} {y-2}Q{x+14} {y-5} {x+5} {y-17}" fill="#f5cc69"/>' for x,y,c in [(16,41,'#b74b55'),(34,35,'#b74b55'),(52,25,'#343845'),(70,35,'#4c936d'),(88,41,'#4c936d')]))

font=ImageFont.truetype(os.environ.get('PICTURE_FONT','/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'),109)
size=128; cols=16; atlas=Image.new('RGBA',(cols*size, math.ceil(len(words)/cols)*size))
index={}
import subprocess
def svg_png(text):
 return subprocess.check_output(["node","-e","require(process.env.PICTURE_SHARP_MODULE || 'sharp')(Buffer.from(process.argv[1])).png().toBuffer().then(b=>process.stdout.write(b))",text])
for i,line in enumerate(words):
 word=line.split('|')[0].upper();tile=Image.new('RGBA',(size,size));index[word]=i
 if word in S:
  assert S[word],word
  import io
  tile=Image.open(io.BytesIO(svg_png(('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">'+S[word]+'</svg>'))))
 elif word in emoji:
  d=ImageDraw.Draw(tile); d.text((64,64),emoji[word],font=font,anchor='mm',embedded_color=True)
 else: raise RuntimeError('Missing picture: '+word)
 atlas.alpha_composite(tile,(i%cols*size,i//cols*size))
(ROOT/'public/art').mkdir(exist_ok=True)
atlas.save(ROOT/'public/art/words.webp',quality=90,method=6)
(ROOT/'src/picture-index.ts').write_text('export const PICTURE_INDEX: Record<string, number> = '+json.dumps(index,separators=(',',':'))+';\nexport const ATLAS_COLUMNS=16;\nexport const ATLAS_ROWS='+str(math.ceil(len(words)/cols))+';\n')
print(f'Created {len(index)} pictures; {len(S)} original vector illustrations; atlas {len((ROOT/"public/art/words.webp").read_bytes())} bytes')
