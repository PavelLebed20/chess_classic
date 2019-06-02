from panda3d.core import PointLight, VBase4, AmbientLight, DirectionalLight, LVector3, Spotlight


class Lights:
    def __init__(self, base, width, height):
        self.base = base
        self.width, self.height = width, height

        self.setup_lights()
        self.light1 = self.init_light(0, -10, 20)
       # self.light2 = self.init_light(0, 10, 20)

        self.base.render.setLight(self.light1)
       # self.base.render.setLight(self.light2)

        self.base.render.setShaderAuto()

    def init_light(self, x, y, z):
        light = self.base.render.attachNewNode(Spotlight("Spot"))
        light.node().setScene(self.base.render)
        light.node().setShadowCaster(True, 1024 * 2, 1024 * 2)
        light.node().getLens().setFov(35)
        #light.node().showFrustum()
        light.node().getLens().setNearFar(10, 30)
        light.setPos(x, y, z)
        light.lookAt(0, 0, 0)
        return light

    def setup_lights(self):  # This function sets up some default lighting
        self.setup_ambient_light()
        #self.setup_point_light(3.5, -3.5, 2)
        #self.setup_point_light(3.5, 3.5, 2)
        #self.setup_point_light(0, 10, 10)
        #self.setup_point_light(0, -5, -5)
        #self.setup_point_light(-3.5, -3.5, 2)
        #self.setup_direct_light(0, 0, -1)

    def setup_ambient_light(self):
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.7, .5, .4, 0.7))
        self.ambient_light = self.base.render.attachNewNode(ambientLight)
        self.base.render.setLight(self.base.render.attachNewNode(ambientLight))

    def setup_direct_light(self, angle_1, angle_2, angle_3, x, y, z):
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(angle_1, angle_2, angle_3))
        directionalLight.setColor((0.6, 0.6, 0.6, 1))
        directionalLight.setShadowCaster(True, 2048, 2048)
        light = self.base.render.attachNewNode(directionalLight)
        self.direct_light.append(light)
        self.base.render.setLight(light)

    def setup_spot_light(self, x, y, z):
        slight = Spotlight('slight')
        slight.setColor(VBase4(1, 1, 1, 1))
        lens = self.base.camLens
        slight.setLens(lens)
        light = self.base.render.attachNewNode(slight)
        light.setPos(x, y, z)
        light.lookAt(0, 0, 0)
        self.direct_light.append(light)
        self.base.render.setLight(light)

    def setup_point_light(self, x, y, z):
        plight = PointLight('plight')
        plight.setColor(VBase4(0.9, 0.9, 0.9, 1))
        light = self.base.render.attachNewNode(plight)
        light.setPos(x, y, z)
        self.point_light.append(light)
        self.base.render.setLight(light)

    def unset(self):
        # turn off lights
        self.base.render.clearLight()
#        for light in self.direct_light:
#            light.removeNode()

#        for light in self.spot_light_node:
#            light.removeNode()

#        for light in self.point_light:
#            light.removeNode()

        if self.ambient_light is not None:
            self.ambient_light.removeNode()
