import pygame


class Drawable:

    def __init__( self ):
        self.__rot = 0
        self.__pos = [0,0,0]

    def get_rot( self ):
        return self.__rot

    def set_rot( self, rot ):
        self.__rot = rot

    def get_pos( self ):
        return self.__pos

    def set_pos( self, pos ):
        self.__pos = pos

    def update( self ):
        pass

    def draw( self ):
        pass



class Image( Drawable ):

    def __init__( self, file ):
        Drawable.__init__(self)
        self.__surf        = None
        self.__surf_bck    = None
        if file: self.load(file)

    def load( self, file ):
        self.__surf = pygame.image.load( file ).convert_alpha()
        self.__surf_bck = self.__surf.copy().convert_alpha()

    def get_size( self ):
        return self.__surf.get_size()

    def set_size( self, size ):
        if size[0] == size[1]:
            self.__surf = pygame.transform.rotozoom(self.__surf_bck, 0, float(size[0]) / float(self.__surf_bck.get_width() ) )

        else:
            self.__surf = pygame.transform.scale(self.__surf_bck, size )

    def update( self ):
        #Drawable.update(self)
        pass

    def draw( self ):
        #Drawable.draw(self)
        pygame.display.get_surface().blit( self.__surf, (self.get_pos()[0], self.get_pos()[1]) )
