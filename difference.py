from PIL import Image, ImageDraw

i = 0
while i < 10:
    print(i)
    f1 = Image.open("renders1/pose_"+str(i)+".png")
    f2 = Image.open("renders/pose_"+str(i)+".png")
    ANS = Image.open("renders1/pose_"+str(i)+".png") 
    draw = ImageDraw.Draw(ANS)
    pix1 = f1.load()
    pix2 = f2.load()
    width = min(f1.size[0], f2.size[0])
    height = min(f1.size[1], f2.size[1])
    eps = 30
    for l in range(width):
        for j in range(height):
            dx1 = pix1[l, j][0] - pix2[l, j][0]
            dx2 = pix1[l, j][1] - pix2[l, j][1]
            dx3 = pix1[l, j][2] - pix2[l, j][2]
            draw.point((l, j), (abs(dx1), abs(dx2), abs(dx3))) 
    ANS.save("difference/pose_"+str(i)+".png", "PNG")
    i+=1
    del draw