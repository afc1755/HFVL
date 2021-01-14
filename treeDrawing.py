import pyglet
from pyglet import shapes
from pyglet.gl import *

window = pyglet.window.Window(400, 600)
batch1 = pyglet.graphics.Batch()
batch2 = pyglet.graphics.Batch()
label = pyglet.text.Label('This is a Christmas Tree',
                          font_name='Times New Roman',
                          font_size=24,
                          x=50, y=50,
                          batch=batch1)
base = shapes.BorderedRectangle(50, 100, 300, 600, border=4, border_color=(255, 255, 255), color=(255, 255, 255),
                                batch=batch1)
base.opacity = 0
trunk = shapes.Rectangle(170, 120, 60, 80, color=(102, 51, 0), batch=batch1)

green_mid_1 = shapes.Rectangle(60, 200, 280, 60, color=(0, 153, 0), batch=batch1)
left_mid_1_vlist = pyglet.graphics.vertex_list(3, ('v2f', [60, 200, 0, 200, 60, 260]))
right_mid_1_vlist = pyglet.graphics.vertex_list(3, ('v2f', [340, 200, 400, 200, 340, 260]))

green_mid_2 = shapes.Rectangle(100, 260, 200, 60, color=(0, 180, 0), batch=batch1)
left_mid_2_vlist = pyglet.graphics.vertex_list(3, ('v2f', [100, 260, 40, 260, 100, 320]))
right_mid_2_vlist = pyglet.graphics.vertex_list(3, ('v2f', [300, 260, 360, 260, 300, 320]))

green_mid_3 = shapes.Rectangle(140, 320, 120, 60, color=(0, 153, 0), batch=batch1)
left_mid_3_vlist = pyglet.graphics.vertex_list(3, ('v2f', [140, 320, 80, 320, 140, 380]))
right_mid_3_vlist = pyglet.graphics.vertex_list(3, ('v2f', [260, 320, 320, 320, 260, 380]))

green_mid_4 = shapes.Rectangle(180, 380, 40, 60, color=(0, 180, 0), batch=batch1)
left_mid_4_vlist = pyglet.graphics.vertex_list(3, ('v2f', [180, 380, 120, 380, 180, 440]))
right_mid_4_vlist = pyglet.graphics.vertex_list(3, ('v2f', [220, 380, 280, 380, 220, 440]))

star = shapes.Rectangle(180, 420, 40, 40, color=(255, 255, 0), batch=batch2)


@window.event
def on_draw():
    window.clear()
    batch1.draw()
    glColor3ub(0, 153, 0)
    left_mid_1_vlist.draw(GL_TRIANGLES)
    right_mid_1_vlist.draw(GL_TRIANGLES)
    left_mid_3_vlist.draw(GL_TRIANGLES)
    right_mid_3_vlist.draw(GL_TRIANGLES)

    glColor3ub(0, 180, 0)
    left_mid_2_vlist.draw(GL_TRIANGLES)
    right_mid_2_vlist.draw(GL_TRIANGLES)
    left_mid_4_vlist.draw(GL_TRIANGLES)
    right_mid_4_vlist.draw(GL_TRIANGLES)

    batch2.draw()


pyglet.app.run()
