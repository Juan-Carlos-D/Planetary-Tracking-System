import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
import pyqtgraph.opengl as gl
from skyfield.api import load

class PlanetTrackerGL(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Planet Tracker with PyQtGraph")
        self.resize(1000, 800)

        self.view = gl.GLViewWidget()
        self.view.setCameraPosition(distance=50)
        self.setCentralWidget(self.view)

        self.planets = load('de421.bsp')
        self.ts = load.timescale()
        self.planet_names = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn']
        self.planet_targets = [self.planets[name] for name in self.planet_names]
        self.planet_colors = [(1, 0.6, 0.0), (1, 1, 0), (0, 0.5, 1), (1, 0.3, 0.3), (0.7, 0.3, 1), (0.9, 0.9, 0.5)]
        self.planet_spheres = []

        stars = gl.GLScatterPlotItem(pos=np.random.uniform(-200, 200, size=(3000, 3)), size=0.4, color=(1, 1, 1, 0.3))
        self.view.addItem(stars)

        self.sun = gl.GLScatterPlotItem(pos=np.array([[0, 0, 0]]), size=6, color=(1, 1, 0, 1))
        self.view.addItem(self.sun)

        for color in self.planet_colors:
            sphere = gl.GLScatterPlotItem(pos=np.array([[0, 0, 0]]), size=2.5, color=color)
            self.view.addItem(sphere)
            self.planet_spheres.append(sphere)

        self.t = self.ts.now()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_positions)
        self.timer.start(30)

    def update_positions(self):
        sun = self.planets['sun']
        self.t = self.ts.tt_jd(self.t.tt + 0.02)

        for i, target in enumerate(self.planet_targets):
            pos = sun.at(self.t).observe(target).position.au
            self.planet_spheres[i].setData(pos=np.array([pos]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tracker = PlanetTrackerGL()
    tracker.show()
    sys.exit(app.exec_())
