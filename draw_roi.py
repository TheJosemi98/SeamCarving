import numpy as np

#Esta funcio dibuja la ROI deseada sobre la imagen. Como parametros de entrada tiene la imagen original y la ROI 
#en formato [x, y, ancho, alto]. Como salida devuelve la imagen con la ROI dibujada

def draw_roi(image, ROI):
  image_roi = np.copy(image)
  for i in range(ROI[3]):
    image_roi[ROI[1], i+ROI[0], 0] = 0.0
    image_roi[ROI[1], i+ROI[0], 1] = 1.0
    image_roi[ROI[1], i+ROI[0], 2] = 0.0

  for i in range(ROI[3]):
    image_roi[ROI[1]+ROI[2], i+ROI[0], 0] = 0.0
    image_roi[ROI[1]+ROI[2], i+ROI[0], 1] = 1.0
    image_roi[ROI[1]+ROI[2], i+ROI[0], 2] = 0.0

  for i in range(ROI[2]):
    image_roi[i+ROI[1], ROI[0], 0] = 0.0
    image_roi[i+ROI[1], ROI[0], 1] = 1.0
    image_roi[i+ROI[1], ROI[0], 2] = 0.0

  for i in range(ROI[2]):
    image_roi[i+ROI[1], ROI[0]+ROI[3], 0] = 0.0
    image_roi[i+ROI[1], ROI[0]+ROI[3], 1] = 1.0
    image_roi[i+ROI[1], ROI[0]+ROI[3], 2] = 0.0
  return image_roi
