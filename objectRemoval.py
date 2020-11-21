import numpy as np
from ImageEnlargeV import getPixelListV
from ImageEnlargeV import getMmatrixV
from ImageEnlargeH import getPixelListH
from ImageEnlargeH import getMmatrixH
from removePixels import removePixels

#Función especifica que elimina los pixeles de una matriz de coste denominada M. A partir de una lista de pixeles y una variable boleana
#que indica si se trata de un seams vertical o horizontal elimina dicho seams en relación con la matriz M introducida
def removePixelsM(M, pixelList, VoH): # VoH: 1 if Vertical, 0 if Horizontal
  pixelList.reverse()

  if(VoH == 1):
    M_result = np.zeros([M.shape[0], M.shape[1]-1])
    for ind_fila in range(M.shape[0]):
      for ind_Colum in range(M.shape[1]-1):
        if(pixelList[ind_fila][1] > ind_Colum):
          M_result[ind_fila, ind_Colum] = M[ind_fila, ind_Colum]
        else:
          M_result[ind_fila, ind_Colum] = M[ind_fila, ind_Colum+1]

  else:
    M_result = np.zeros([M.shape[0]-1, M.shape[1]])
    for ind_Colum in range(M.shape[1]):
      for ind_fila in range(M.shape[0]-1):
        if(pixelList[ind_Colum][0] > ind_fila):
          M_result[ind_fila, ind_Colum] = M[ind_fila, ind_Colum]
        else:
          M_result[ind_fila, ind_Colum] = M[ind_fila+1, ind_Colum]

  return M_result


#Función especifica que obtiene una imagen con los pixeles eliminados de una determinada una ROI definida, indicando la posición de la 
#esquina superior izquierda y las dimensiones de dicha región. También se introduce la imagen de donde queremos eliminar los pixeles, 
#obteniendo de este metodo la imagen resultado 
def objectRemoval(image, ROI):
  pos = (ROI[1], ROI[0])
  dim = (ROI[2], ROI[3])

  filas = image.shape[0]
  columnas = image.shape[1]

  if(pos[0]+dim[0] > filas or pos[1]+dim[1] > columnas):
    print('Incorrect target section')
    return image
  else:
    if(dim[0] < dim[1]):
        VoH = False
        NumIter = dim[0]
        M = getMmatrixH(image[:,:,0])   
    else:
        VoH = True
        NumIter = dim[1]
        M = getMmatrixV(image[:,:,0])

    image_resultado = image

    for i in range(image.shape[0]):
      for j in range(image.shape[1]):
          
        if(VoH):
            if( (i >= pos[0] and i <= pos[0]+dim[0]) and (j >= pos[1] and j <= pos[1]+dim[1])):
              M[i,j] = -1e20
            elif( (i >= pos[0] and i <= pos[0]+dim[0]) and (j < pos[1] or j >= pos[1]+dim[1]) ):
              M[i,j] = M[i,j] + 1e20
            elif( (i > pos[0] + dim[0]) and (j < pos[1] - (i - (pos[0] + dim[0])))):
              M[i,j] = M[i,j] + 1e20
            elif( (i > pos[0] + dim[0]) and (j > (pos[1] + dim[1]) + (i - (pos[0] + dim[0])))):
              M[i,j] = M[i,j] + 1e20
            else:
              M[i,j] = M[i,j] - 100           
        else:
            if( (i >= pos[0] and i <= pos[0]+dim[0]) and (j >= pos[1] and j <= pos[1]+dim[1]) ):
              M[i,j] = -1e20
            elif((i < pos[0] or i > pos[0]+dim[0] ) and ( j >= pos[1] and j <= pos[1]+dim[1])):
              M[i,j] = M[i,j] + 1e20
            elif( ( j > pos[1] + dim[1]) and ( i <  pos[0] - (j - (pos[1] + dim[1]))) ):
              M[i,j] = M[i,j] + 1e20
            elif( ( j > pos[1] + dim[1]) and ( i >  pos[0] + dim[0] + (j - (pos[1] + dim[1]))) ):
              M[i,j] = M[i,j] + 1e20
            else:
              M[i,j] = M[i,j] - 100
            

    for k in range(NumIter):
      if(VoH == False):
        pixelList = getPixelListH(M)
        image_resultado = removePixels(image_resultado,pixelList,VoH)
        M = removePixelsM(M, pixelList, VoH)
      else:
        pixelList =getPixelListV(M)
        image_resultado = removePixels(image_resultado,pixelList,VoH)
        M = removePixelsM(M, pixelList, VoH)

    return image_resultado