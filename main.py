from kivy.graphics import Rectangle
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
import kivy
import grafo_laberinto

kivy.require("2.2.0")

def collides(rect1,rect2):
    r1x = rect1[0][0]#posicion en eje x del objeto que va a colisionar
    r1y = rect1[0][1]#posicion en eje y del objeto que va a colisionar
    r2x = rect2[0][0]#posicion en eje x del objeto que va a ser colisionado
    r2y = rect2[0][1]#posicion en eje y del objeto que va a ser colisionado
    r1w = rect1[1][0]#ancho del objeto que va a colisionar
    r1h = rect1[1][1]#altura del objeto que va a colisionar
    r2w = rect2[1][0]#ancho del objeto que va a ser colisionado
    r2h = rect2[1][1]#altura del objeto que va a ser colisionado
    if (r1x < r2x + r2w  and r1x + r1w > r2w and r1y < r2y + r2h and r1y + r1h > r2y):
        return True
    else:
        return False
    
class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.map=grafo_laberinto.matriz
        height=Window.height
        width=Window.width
        relationship=2
        self.direccion=""
        Window.size = (relationship*height,height)
        Window.rotation = 0
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed,self)
        self._keyboard.bind(on_key_down=self.on_key_down)
        self._keyboard.bind(on_key_up=self.on_key_up)
        self.map = grafo_laberinto.matriz
        self.keysPressed= set()
        Clock.schedule_interval(self.move_step,0)
        self.obstacles=[]
        with self.canvas:
            for i in range(len(self.map)):
                for j in range(len(self.map[i])):
                    if self.map[i][j] == "x":
                        self.obstacle=Rectangle(source="images/rock.png",pos=(80+80*i,80+80*j), size=(80,80))
                        self.obstacles.append(self.obstacle)                    
                    elif self.map[i][j] == "p":
                        self.player = Rectangle(source="images/1.png",pos=(80+80*i,80+80*j),size=(60,60))

        
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_key_down)
        self._keyboard.unbind(on_key_up=self.on_key_up)
        self._keyboard=None
        
    def on_key_down(self,keyboard,keycode,text,modifiers):
        self.keysPressed.add(text)

    def on_key_up(self, keyboard,keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)
                
    def move_step(self, dt):
        currentx = self.player.pos[0]
        currenty = self.player.pos[1]
        step_size = 60 * dt
        if "w" in self.keysPressed:
            self.direccion = "Arriba"
            currenty += step_size
            self.player.source="images/2.png"
        elif "s" in self.keysPressed:
            self.direccion = "Abajo"
            currenty -= step_size
            self.player.source="images/4.png"
        elif "a" in self.keysPressed:
            self.direccion = "Izquierda"
            currentx -= step_size
            self.player.source="images/1.png"
        elif "d" in self.keysPressed:
            self.direccion= "Derecha"
            currentx += step_size
            self.player.source="images/3.png"
        for obstacle in self.obstacles:
            if collides((self.player.pos,self.player.size),(obstacle.pos,obstacle.size)):
                if collides((obstacle.pos,obstacle.size),(self.player.pos,self.player.size)):
                    if self.direccion=="Arriba":
                        currenty=self.player.pos[1]-1
                    if self.direccion=="Abajo":
                        currenty=self.player.pos[1]+1
                    if self.direccion=="Derecha":
                        currentx=self.player.pos[0]-1
                    if self.direccion=="Izquierda":
                        currentx=self.player.pos[0]+1
        self.player.pos = (currentx,currenty)

class MyApp(App):
    def build(self):
        return GameWidget()


if __name__ == '__main__':
    MyApp().run()
