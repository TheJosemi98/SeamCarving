from skimage import io
import numpy as np
import scipy.signal

#Modifica la matriz M segun una lista de pixeles. Introduce un coste muy alto en dichos pixeles.
def modMatrix(M, pixelList):
  for i in range(len(pixelList)):
    M[pixelList[i][0], pixelList[i][1]] = 1e20

  return M

#Devuelve la matriz M para seams verticales. Procedimiento similar al de la funcion SeamCarving.py
def getMmatrixV(image): #Imagen 2D

  #Sobel's filter
  Gx = np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]])
  Gy = np.transpose(Gx)

  Ix = scipy.signal.convolve2d(image, Gx, mode='same')
  Iy = scipy.signal.convolve2d(image, Gy, mode='same')

  #Energy operator
  e = abs(Ix) + abs(Iy)

  #Vertical Seam
  M = np.zeros(e.shape)

  for i in range(e.shape[0]): #Rows
    for j in range(e.shape[1]): #Columns

      if (i-1)>=0 and (j-1)>=0:
        e1 = M[i-1,j-1]
      else:
        e1 = 1e20

      if (i-1)>=0:
        e2 = M[i-1,j]
      else:
        e2 = 1e20

      if (i-1)>=0 and (j+1)<=(e.shape[1]-1):
        e3 = M[i-1,j+1]
      else:
        e3 = 1e20

      if e1==1e20 and e2==1e20 and e3==1e20:
        M[i,j] = e[i,j]
      else:
        M[i,j] = e[i,j] + min(e1,e2,e3)
  return M

#Devuelve la lista de pixeles a eliminar según la matriz M en vertical.
def getPixelListV(M):
  pixelListV = []
  pixelListV.append((M.shape[0]-1, np.argmin(M[M.shape[0]-1])))

  i = M.shape[0]-1
  j = np.argmin(M[M.shape[0]-1])

  while i!=0:
    e1 = M[i-1, j]

    if (j-1)<0:
      e2 = 1e20
    else:
      e2 = M[i-1, j-1]

    if (j+1)>M.shape[1]-1:
      e3 = 1e20
    else:
      e3 = M[i-1, j+1]

    min_pos = np.argmin([e1, e2, e3])

    if min_pos == 0:
      pixelListV.append((i-1, j))
    if min_pos == 1:
      pixelListV.append((i-1, j-1))
      j = j-1
    if min_pos == 2:
      pixelListV.append((i-1, j+1))
      j = j+1

    i -= 1
  return pixelListV

#Calcula un determinado numero de seams verticales. Como entrada tiene la matriz M y k, el numero de filas a añadir
def multipleSeamsV(M, k):
  Matrix = M
  pixelList = getPixelListV(Matrix) #Obtiene la lista de pixeles a añadir
  pixelList.reverse()
  Matrix = modMatrix(Matrix, pixelList) #Les asigna a dichos pixeles un coste muy alto
  vpixelList = np.expand_dims(np.array(pixelList)[:,1], axis=0)

  for i in range(k-1): #Mismo proceso k-1 veces repetido. Hasta obtener el numero de seams deseado.
    pixelList = getPixelListV(Matrix)
    pixelList.reverse()
    Matrix = modMatrix(Matrix, pixelList)
    vpixelList = np.vstack((vpixelList, np.expand_dims(np.array(pixelList)[:,1], axis=0)))

  return vpixelList

#Duplica los Seams verticales calculados previamente. Como entrada tiene la imagen original y una matriz con seams.
def duplicateSeamV(image, vSeam):
  resized_image = np.zeros((image.shape[0], image.shape[1]+1, image.shape[2]))
  resized_j = 0
  for i in range(image.shape[0]):    #Se realiza el duplicado de pixeles
    for j in range(image.shape[1]):
      if (j==vSeam[:,i]):
        resized_image[i, resized_j, 0] = image[i, j, 0]
        resized_image[i, resized_j+1, 0] = image[i, j, 0]

        resized_image[i, resized_j, 1] = image[i, j, 1]
        resized_image[i, resized_j+1, 1] = image[i, j, 1]

        resized_image[i, resized_j, 2] = image[i, j, 2]
        resized_image[i, resized_j+1, 2] = image[i, j, 2]
        resized_j += 2
      else:
        resized_image[i,resized_j, 0] = image[i, j, 0]
        resized_image[i,resized_j, 1] = image[i, j, 1]
        resized_image[i,resized_j, 2] = image[i, j, 2]
        resized_j += 1
    resized_j = 0
  return resized_image

#Alarga la imagen verticales. Funcion que realiza todas las operaciones necesarias para ampliar imagenes.
def ImageEnlargeV(image, k):
  image_original = image
  image = image[:,:,0]

  M = getMmatrixV(image) #Calculo de la matriz M
  resized_image = np.copy(image_original)
  SeamsMatrix = multipleSeamsV(M, k) #Calculo de los seams a duplicar
  Seams = SeamsMatrix

  for i in range(k):
    pos = np.argmin(SeamsMatrix[:,0]) #Seleecciona el seam situado mas a la izquierda
    seam = np.expand_dims(SeamsMatrix[pos,:], axis=0)
    resized_image = duplicateSeamV(resized_image, seam) #Duplica los pixel del seam
    SeamsMatrix = np.delete(SeamsMatrix, pos, axis=0) + 1 #Elimina el seam de la matriz de seam. Suma uno para
  return resized_image, Seams                             #desplazar el resto de seams porque la imagen cambia de tamaño
