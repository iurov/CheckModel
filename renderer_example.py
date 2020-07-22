from renderer import Renderer
from strike_utils import *


save = True
rotx = [0, np.pi/2, np.pi, 3*np.pi/2, 0, 0, np.pi/4, np.pi/4, np.pi/-4, np.pi/-4]
roty = [0, 0, 0, 0, np.pi/2, -np.pi/2, 0, 0, 0, 0]
rotz = [0, 0, 0, 0, 0, 0, np.pi/4, np.pi/-4, np.pi/4, np.pi/-4]

def rendering_ex(fobj, fmtl):
    renderer = ""
    renderer = Renderer(
        fobj, fmtl
    )

    renderer.prog["x"].value = 0
    renderer.prog["y"].value = 0
    renderer.prog["z"].value = -8


    for i in range(len(rotx)):
        R_obj = gen_rotation_matrix(rotx[i], roty[i], rotz[i])
        renderer.prog["R_obj"].write(R_obj.T.astype("f4").tobytes())
        image = renderer.render()
        # print(i)
        if save:
            image.save("renders1/pose_"+str(i)+".png")
        else:
            image.show()

    