import numpy as np

#Esta funcion elimina pixeles de una imagen a partir de una lista de pixeles dada. Como entrada tiene la imagen original
#la lista de pixeles, y una variable booleana indicando se se realiza vertical u horizontalmente.

def removePixels(image, pixelList, VoH): # VoH: 1 if Vertical, 0 if Horizontal
  pixelList.reverse()

  if(VoH == 1):
    resized_image = np.zeros([image.shape[0], image.shape[1]-1, 3])

    for ind_fila in range(image.shape[0]):
      for ind_Colum in range(image.shape[1]-1):
        if(pixelList[ind_fila][1] > ind_Colum):                             
          resized_image[ind_fila, ind_Colum, 0] = image[ind_fila, ind_Colum, 0]
          resized_image[ind_fila, ind_Colum, 1] = image[ind_fila, ind_Colum, 1]
          resized_image[ind_fila, ind_Colum, 2] = image[ind_fila, ind_Colum, 2]
        else:                                                                   
          resized_image[ind_fila, ind_Colum, 0] = image[ind_fila, ind_Colum+1, 0]
          resized_image[ind_fila, ind_Colum, 1] = image[ind_fila, ind_Colum+1, 1]
          resized_image[ind_fila, ind_Colum, 2] = image[ind_fila, ind_Colum+1, 2]
  else:
    resized_image = np.zeros([image.shape[0]-1, image.shape[1], 3])

    for ind_Colum in range(image.shape[1]):
      for ind_fila in range(image.shape[0]-1):             
        if(pixelList[ind_Colum][0] > ind_fila):
          resized_image[ind_fila, ind_Colum, 0] = image[ind_fila, ind_Colum, 0]
          resized_image[ind_fila, ind_Colum, 1] = image[ind_fila, ind_Colum, 1]
          resized_image[ind_fila, ind_Colum, 2] = image[ind_fila, ind_Colum, 2]

        else:          
          resized_image[ind_fila, ind_Colum, 0] = image[ind_fila+1, ind_Colum, 0]
          resized_image[ind_fila, ind_Colum, 1] = image[ind_fila+1, ind_Colum, 1]
          resized_image[ind_fila, ind_Colum, 2] = image[ind_fila+1, ind_Colum, 2]

  return resized_image
