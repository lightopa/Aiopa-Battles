__tags__ = ['array']

exclude = False

try:
    import pygame.mixer
    import numpy
except ImportError:
    try:
        import Numeric
        import pygame._numericsndarray
    except ImportError:
        exclude = True

if exclude:
    __tags__.extend(('ignore', 'subprocess_ignore'))
