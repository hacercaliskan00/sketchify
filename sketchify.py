import numpy as np
import imageio
import cv2
from scipy.ndimage import gaussian_filter

img = "friends.jpg"

def rgb2gray(rgb):
    # Doğru ağırlıklarla gri tonlamaya dönüştürme
    return np.dot(rgb[...,:3], [0.2989, 0.587, 0.114])

def dodge(front, back):
    final_sketch = front * 255 / (255 - back)
    final_sketch[final_sketch > 255] = 255
    final_sketch[back == 255] = 255
    return final_sketch.astype("uint8")

# Resim okundu
ss = imageio.imread(img)
gray = rgb2gray(ss)

# Ters görüntü alındı
i = 255 - gray

# Gaussian bulanıklık uygulandı
blur = gaussian_filter(i, sigma=4)

# Dodge işlemi uygulandı
r = dodge(blur, gray)

# Kenar tespiti yapıldı
edges = cv2.Canny(gray.astype("uint8"), 50, 150)
r = cv2.addWeighted(r, 0.85, edges, 0.15, 0)

# Kontrast arttırıldı
r = cv2.normalize(r, None, 0, 255, cv2.NORM_MINMAX)


# Son çıktı kaydedildi
cv2.imwrite("sketch_friends.png", r)
