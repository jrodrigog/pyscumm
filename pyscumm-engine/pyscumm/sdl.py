import pygame, euclid
from euclid import Vector2


class Drawable(object):

    def __init__(self):
        self._image = None
        self._image_bck = None
        self.screen_position = Vector2(0, 0)

    def set_image(self, img):
        self._image = img
        self._image_bck = img.copy()
        self._collider = self._image.get_rect(topleft=self.screen_position) # Dont apply the topleft!! bug

    def get_image(self):
        return self._image

    def scale(self, value):
        # NEED ALSO SCALE THE RECT !!
        self._image = pygame.transform.rotozoom(self._image_bck, 0, value)

    def rotate(self, angle):
        # NEED ALSO ROTATE THE RECT !!
        self._image = pygame.transform.rotate(self._image_bck, angle)

    def draw(self):
        pygame.display.get_surface().blit(self._image, self.screen_position)

    image = property(get_image, set_image)