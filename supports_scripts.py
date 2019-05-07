from direct.showbase.ShowBase import ShowBase
from pandac import *
from direct import *
from panda3d.core import *
from direct.showbase.Loader import *
import direct.directbase.DirectStart

# http://www.custommapmakers.org/skyboxes.php

class SkySphere(ShowBase):
    def __init__(self):
        self.sphere = loader.loadModel("ChessRender/data/InvertedSphere.egg")
        # Load a sphere with a radius of 1 unit and the faces directed inward.

        self.sphere.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
        self.sphere.setTexProjector(TextureStage.getDefault(), render, self.sphere)
        self.sphere.setTexPos(TextureStage.getDefault(), 0, 0, 0)
        self.sphere.setTexScale(TextureStage.getDefault(), .5)
        # Create some 3D texture coordinates on the sphere. For more info on this, check the Panda3D manual.

        tex = loader.loadCubeMap("ChessRender/data/cube_map/sist_#.jpg")
        self.sphere.setTexture(tex)
        # Load the cube map and apply it to the sphere.

        self.sphere.setLightOff()
        # Tell the sphere to ignore the lighting.

        self.sphere.setScale(1000)
        # Increase the scale of the sphere so it will be larger than the scene.

        self.sphere.reparentTo(render)
        # Reparent the sphere to render so you can see it.

        result = self.sphere.writeBamFile("Sist.bam")
        # Save out the bam file.
        print(result)
    # Print out whether the saving succeeded or not.


SS = SkySphere()
run()