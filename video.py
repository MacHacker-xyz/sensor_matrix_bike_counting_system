import cv2
fps = 20 #视频每秒10帧
size = (640,480) #需要转为视频的图片的尺寸,  可以使用cv2.resize()进行修改

video = cv2.VideoWriter("Video.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)   #视频保存在当前目录下, 格式为 motion-jpeg codec，图片颜色失真比较小

for i in range(1000):
    img = cv2.imread("picture/{}.jpg".format(i))
    video.write(img)

video.release()
cv2.destroyAllWindows()
print('Video has been made.')
