"""
Example showing how to create particle explosions via the GPU.
"""
import math
from array import array
from dataclasses import dataclass
import arcade
import arcade.gl
import random
import time
import OpenGL.GL as gl

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN_TITLE = "fireworks"
PARTICLE_COUNT = 300
MIN_FADE_TIME = 3
MAX_FADE_TIME = 5

@dataclass
class Burst:
    """ Track for each burst. """
    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry

    start_time: float

class Firework(arcade.Sprite):
    def __init__(self, path, ctx, burst_list):
        super().__init__(path)
        self.center_x = random.randint(0, SCREEN_WIDTH)
        self.center_y = 0
        self.vel_x = random.uniform(-5.0, 5.0)
        self.target_y = random.uniform(300.0, 500.0)
        self.fading_out = False
        self.alpha = 255
        self.ctx = ctx
        self.burst_list = burst_list

    def update(self):
        if not self.fading_out:
            self.center_y += 10
            if self.center_y >= self.target_y:
                self.fading_out = True
        else:
            self.alpha -= 5
            if self.alpha <= 0:
                self.boom()
                self.kill()
    
    def boom(self):
        def _gen_initial_data(initial_x, initial_y):
            """ Generate data for each particle """
            for i in range(PARTICLE_COUNT):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(0.0, 0.3)
                radius = random.uniform(0, 1) ** 0.5  # Distance from center (random point on unit circle)
                dx = math.sin(angle) * speed * radius
                dy = math.cos(angle) * speed * radius
                # red = random.uniform(0.6, 1.0)
                red = 1
                green = random.uniform(0.1, 1.0)
                blue = random.uniform(0.1, 1.0)
                fade_rate = random.uniform(1 / MAX_FADE_TIME, 1 / MIN_FADE_TIME)
            
                yield initial_x
                yield initial_y
                yield dx
                yield dy
                yield red
                yield green
                yield blue
                yield fade_rate
    
        # Recalculate the coordinates from pixels to the OpenGL system with
        # 0, 0 at the center.
        x2 = self.center_x / self.width * 2. - 1.
        y2 = self.center_y / self.height * 2. - 1. + 50
    
        # Get initial particle data
        initial_data = _gen_initial_data(x2, y2)
    
        # Create a buffer with that data
        buffer = self.ctx.buffer(data=array('f', initial_data))
    
        # Create a buffer description that says how the buffer data is formatted.
        buffer_description = arcade.gl.BufferDescription(buffer,
                                                         '2f 2f 3f f',
                                                         ['in_pos',
                                                          'in_vel',
                                                          'in_color',
                                                          'in_fade_rate'])
        # Create our Vertex Attribute Object
        vao = self.ctx.geometry([buffer_description])
    
        # Create the Burst object and add it to the list of bursts
        burst = Burst(buffer=buffer, vao=vao, start_time=time.time())
        self.burst_list.append(burst)
        
class MyWindow(arcade.Window):
    """ Main window"""
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.ctx.enable_only(self.ctx.BLEND)
        self.burst_list = []

        # Program to visualize the points
        self.program = self.ctx.load_program(
            vertex_shader="shader/demo3.glsl",
            fragment_shader="shader/demo2.glsl",
        )

        self.ctx.enable_only()
        
        self.fireworks = arcade.SpriteList()
    
        # self.fireworks.append(Firework('images/fireworks/firework.jpeg', self.ctx, self.burst_list))

        # self.background = arcade.load_texture('images/background/star_sky.jpg')
        
    def on_draw(self):
        """ Draw everything """
        self.clear()

        # 只启用部分OpenGL扩展
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # Set the particle size
        self.ctx.point_size = 2 * self.get_pixel_ratio()

        # Loop through each burst
        for burst in self.burst_list:


            # Set the uniform data

            self.program['time'] = time.time() - burst.start_time


            # Render the burst
            burst.vao.render(self.program, mode=self.ctx.POINTS)
        
        self.fireworks.draw()
        # arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
        #                               SCREEN_WIDTH, SCREEN_HEIGHT, self.background, 0)

    def on_update(self, dt):
        """ Update everything """
        
        self.fireworks.update()
    
        temp_list = self.burst_list.copy()

        for burst in temp_list:

            if time.time() - burst.start_time > MAX_FADE_TIME:
                self.burst_list.remove(burst)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """ User clicks mouse """

        def _gen_initial_data(initial_x, initial_y):
            """ Generate data for each particle """
            for i in range(PARTICLE_COUNT):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(0.0, 0.3)
                radius = random.uniform(0, 1) ** 0.5  # Distance from center (random point on unit circle)
                dx = math.sin(angle) * speed * radius
                dy = math.cos(angle) * speed * radius
                # red = random.uniform(0.6, 1.0)
                red = 1
                green = random.uniform(0.1, 1.0)
                blue = random.uniform(0.1, 1.0)
                fade_rate = random.uniform(1 / MAX_FADE_TIME, 1 / MIN_FADE_TIME)
        
                yield initial_x
                yield initial_y
                yield dx
                yield dy
                yield red
                yield green
                yield blue
                yield fade_rate

        # Recalculate the coordinates from pixels to the OpenGL system with
        # 0, 0 at the center.
        x2 = x / self.width * 2. - 1.
        y2 = y / self.height * 2. - 1.

        # Get initial particle data
        initial_data = _gen_initial_data(x2, y2)

        # Create a buffer with that data
        buffer = self.ctx.buffer(data=array('f', initial_data))

        # Create a buffer description that says how the buffer data is formatted.
        buffer_description = arcade.gl.BufferDescription(buffer,
                                                         '2f 2f 3f f',
                                                         ['in_pos',
                                                          'in_vel',
                                                          'in_color',
                                                          'in_fade_rate'])
        # Create our Vertex Attribute Object
        vao = self.ctx.geometry([buffer_description])

        # Create the Burst object and add it to the list of bursts
        burst = Burst(buffer=buffer, vao=vao, start_time=time.time())
        self.burst_list.append(burst)


window = MyWindow()
window.center_window()

arcade.run()