def txtf(param = "SSIMM"):
    import comare
    import renderer_example

    from os import listdir
    from os.path import isfile, join
    from renderer import Renderer

    files= [f for f in listdir("objects/izbstri") if isfile(join("izbs", f))]
    if param == "SSIMM":
        st = open("statm.txt", "a")
    if param == "MS-SSIM":
        st = open("statms.txt", "a")
    if param == "G-SIMM":
        st = open("statg.txt", "a")
    if param == "SSIM":
        st = open("stat.txt", "a")
    st.close()
    i = 0
    for f in files:
        print(f)
        print(i)
        renderer_example.rendering_ex("objects/izbstri/"+f, "solve.mtl")
        if param == "SSIMM":
            comare.rez("SSIMM")
        if param == "MS-SSIM":
            comare.rez("MS-SSIM")
        if param == "G-SIMM":
            comare.rez("G-SIMM")
        if param == "SSIM":
            comare.rez("SSIM")
        i+=1

def bar(param = "SSIMM"):
    import numpy as np
    import matplotlib.pyplot as plt

    if param == "SSIMM":
        fname = 'statm.txt'
    if param == "MS-SSIM":
        fname = 'statms.txt'
    if param == "G-SSIM":
        fname = 'statg.txt'
    if param == "SSIM":
        fname = 'stat.txt'
    a = np.loadtxt(fname)
    y = np.random.randint(1, 20, size = 70)
    with open('stat.txt') as f:
        s = sum(1 for _ in f)

    fig, ax = plt.subplots()

    ax.bar(np.arange(0, s), a, label = 'Баллы')

    ax.set_facecolor('seashell')
    plt.ylabel("Баллы", fontsize=16)
    fig.set_facecolor('floralwhite')
    fig.set_figwidth(12)    #  ширина Figure
    fig.set_figheight(6)    #  высота Figure

    plt.show()


def circle(param = "SSIMM"):
    import numpy as np
    import matplotlib.pyplot as plt

    if param == "SSIMM":
        fname = 'statm.txt'
    if param == "MS-SSIM":
        fname = 'statms.txt'
    if param == "G-SSIM":
        fname = 'statg.txt'
    if param == "SSIM":
        fname = 'stat.txt'
    a = np.loadtxt(fname)
    x85 = 0
    x70 = 0
    x50 = 0
    x0 = 0
    for i in a:
        if i>=85:
            x85+=1
        else:
            if i>=70:
                x70+=1
            else:
                if i>=50:
                    x50+=1
                else:
                    x0+=1
    vals = [x0, x70,  x50, x85]
    labels = ["0-49","70-84", "50-69", "85-100" ]
    fig, ax = plt.subplots(dpi = 200)
    ax.pie(vals, autopct='%1.1f%%')
    ax.axis("equal")
    ax.legend(loc="best",  labels=labels)
    plt.show()

def scat(param = "SSIMM"):
    import numpy as np
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots()

    if param == "SSIMM":
        fname = 'statm.txt'
    if param == "MS-SSIM":
        fname = 'statms.txt'
    if param == "G-SSIM":
        fname = 'statg.txt'
    if param == "SSIM":
        fname = 'stat.txt'
    a = np.loadtxt(fname)
    with open(fname) as f:
        s = sum(1 for _ in f)
    print (s)

    ax.scatter( np.arange(0, s), a)    #  цвет точек

    ax.set_title('Градиентный SSIM')     #  заголовок для Axes

    fig.set_figwidth(8)     #  ширина и
    fig.set_figheight(8)    #  высота "Figure"

    plt.show()

bar("SSIM")