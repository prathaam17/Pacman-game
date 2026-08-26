import pygame
import os

class AssetManager:
    _images = {}
    _fonts = {}

    @classmethod
    def get_image(cls, path, size=None):
        key = (path, size)
        if key in cls._images:
            return cls._images[key]
        
        if os.path.exists(path):
            img = pygame.image.load(path)
            if size:
                img = pygame.transform.scale(img, size)
            cls._images[key] = img
            return img
        else:
            # Fallback surface if asset file is missing
            surf = pygame.Surface(size if size else (32, 32))
            surf.fill((255, 0, 255))
            cls._images[key] = surf
            return surf

    @classmethod
    def get_font(cls, size, font_name=None):
        key = (font_name, size)
        if key in cls._fonts:
            return cls._fonts[key]
        
        font = pygame.font.SysFont(font_name if font_name else "Arial", size, bold=True)
        cls._fonts[key] = font
        return font
