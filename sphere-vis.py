import sys

from vispy import scene
from vispy.visuals.transforms import STTransform

canvas = scene.SceneCanvas(keys='interactive', bgcolor='white', size=(800, 800), show=True)

view = canvas.central_widget.add_view()
view.camera = "arcball"

sphere1 = scene.visuals.Sphere(radius=1, method="latitude", parent=view.scene, edge_color="red")

sphere2 = scene.visuals.Sphere(radius=1, method="ico", parent=view.scene, edge_color="red")

sphere3 = scene.visuals.Sphere(radius=1, method="cube", parent=view.scene, edge_color="red")

sphere1.transform = STTransform(translate=[-2.5, 0, 0])
sphere3.transform = STTransform(translate=[2.5, 0, 0])

view.camera.set_range(x=[-3, 3])

if __name__ == '__main__':
    canvas.app.run()