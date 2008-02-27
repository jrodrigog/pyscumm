from sdl import Drawable
from base import debugger
from engine import engine
from euclid import Vector3


class BaseObject(object):

    def __init__(self):
        self._collider = None
        self.position = Vector3(0, 0, 0)
        self.description = 'NotDescripted'

    def update(self):
        # Update the Drawable screen_position with the camera position of the room
        camera = engine.room.camera
        self.screen_position = self.position - (camera.position.x, camera.position.y, 0)
        self.screen_position = self.screen_position[:2]
        self._collider.topleft = self.screen_position

    def get_collider(self):
        return self._collider

    collider = property(get_collider, None)



class Item(Drawable, BaseObject):

    def __init__(self):
        Drawable.__init__(self)
        BaseObject.__init__(self)

    def on_look(self):
        debugger.warn('on_look() method called. NotImplemented')

    def on_get(self):
        debugger.warn('on_get() method called. NotImplemented')

    def on_talk(self):
        debugger.warn('on_talk() method called. NotImplemented')