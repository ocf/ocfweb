import os
import sys

# argument syntax: python3 generate-font-faces.py FOLDER1 FOLDER2 FOLDER3
# you may have to remove the variable syntax ttfs
# also remove the compressed files

WEIGHTS = [
        'Thin',
        'ExtraLight',
        'Light',
        'Regular',
        'Medium',
        'SemiBold',
        'Bold',
        'ExtraBold',
        'Black',
]

with open('font-faces.css', 'w') as css:
    for direc in sys.argv[1:]:
        for file in os.listdir('./' + direc):
            if file.split('.')[-1] != 'ttf':
                continue

            weight = 0
            for i in range(len(WEIGHTS)):
                if WEIGHTS[i] in file:
                    weight = 100*(i+1)

            css.write(
                """
@font-face {{
    font-family: "{family}";
    font-style: {style};
    font-weight: {weight};
    font-display: swap;
    font-width: 100%;
    src: url("{path}") format("ttf");
}}""".format(
                    family=direc[:-1].replace('_', ' '),
                    style=('italic' if 'italic' in file.lower() else 'normal'),
                    weight=weight,
                    path='./'+direc+file,
                ),
            )
