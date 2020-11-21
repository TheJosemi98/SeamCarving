from skimage import io
import numpy as np
import scipy.signal

#Modifica la matriz M segun una lista de pixeles. Introduce un coste muy alto en dichos pixeles.
def modMatrix(M, pixelList):
  for i in range(len(pixelList)):
    M[pixelList[i][0], pixelList[i][1]] = 1e20

  return M

#Devuelve la matriz M para seams horizontales. Procedimiento similar al de la funcion SeamCarving.py
def getMmatrixH(image):

  #Sobel's filter
  Gx = np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]])
  Gy = np.transpose(Gx)

  Ix = scipy.signal.convolve2d(image, Gx, mode='same')
  Iy = scipy.signal.convolve2d(image, Gy, mode='same')

  #Energy operator
  e = abs(Ix) + abs(Iy)

  #Vertical Seam
  M = np.zeros(e.shape)

  for j in range(e.shape[1]): #Columns
    for i in range(e.shape[0]): #Rows

      if (i-1)>=0 and (j-1)>=0:
        e1 = M[i-1,j-1]
      else:
        e1 = 1e20

      if (j-1)>=0:
        e2 = M[i,j-1]
      else:
        e2 = 1e20

      if (j-1)>=0 and (i+1)<=(e.shape[0]-1):
        e3 = M[i+1,j-1]
      else:
        e3 = 1e20

      if e1==1e20 and e2==1e20 and e3==1e20:
        M[i,j] = e[i,j]
      else:
        M[i,j] = e[i,j] + min(e1,e2,e3)
  return M

#Devuelve la lista de pixeles a eliminar según la matriz M en horizontal.
def getPixelListH(M):
  pixelListH = []
  pixelListH.append((np.argmin(M[:,M.shape[1]-1]), M.shape[1]-1))

  i = np.argmin(M[:,M.shape[1]-1])
  j = M.shape[1]-1

  while j!=0:
    e1 = M[i, j-1]

    if (i-1)<0:
      e2 = 1e20
    else:
      e2 = M[i-1, j-1]

    if (i+1)>M.shape[0]-1:
      e3 = 1e20
    else:
      e3 = M[i+1, j-1]

    min_pos = np.argmin([e1, e2, e3])

    if min_pos == 0:
      pixelListH.append((i, j-1))
    if min_pos == 1:
      pixelListH.append((i-1, j-1))
      i = i-1
    if min_pos == 2:
      pixelListH.append((i+1, j-1))
      i = i+1

    j -= 1
  return pixelListH


#Calcula un determinado numero de seams horizontales. Como entrada tiene la matriz M y k, el numero de filas a añadir
def multipleSeamsH(M, k):
  Matrix = M
  pixelList = getPixelListH(Matrix) #Obtiene la lista de pixeles a añadir
  pixelList.reverse()
  Matrix = modMatrix(Matrix, pixelList) #Les asigna a dichos pixeles un coste muy alto
  hpixelList = np.expand_dims(np.array(pixelList)[:,0], axis=0) 

  for i in range(k-1): #Mismo proceso k-1 veces repetido. Hasta obtener el numero de seams deseado.
    pixelList = getPixelListH(Matrix)
    pixelList.reverse()
    M = modMatrix(Matrix, pixelList)
    hpixelList = np.vstack((hpixelList, np.expand_dims(np.array(pixelList)[:,0], axis=0)))

  return hpixelList

#Duplica los Seams horizontales calculados previamente. Como entrada tiene la imagen original y una matriz con seams.
def duplicateSeamH(image, hSeam):
  resized_image = np.zeros((image.shape[0]+1, image.shape[1], image.shape[2]))
  resized_i = 0
  for j in range(image.shape[1]): #Columna      #Se realiza el duplicado de pixeles
    for i in range(image.shape[0]): #Fila
      if (i==hSeam[:,j]):
        resized_image[resized_i, j, 0] = image[i, j, 0]
        resized_image[resized_i+1, j, 0] = image[i, j, 0]

        resized_image[resized_i, j, 1] = image[i, j, 1]
        resized_image[resized_i+1, j, 1] = image[i, j, 1]

        resized_image[resized_i, j, 2] = image[i, j, 2]
        resized_image[resized_i+1, j, 2] = image[i, j, 2]
        resized_i += 2
      else:
        resized_image[resized_i,j, 0] = image[i, j, 0]
        resized_image[resized_i,j, 1] = image[i, j, 1]
        resized_image[resized_i,j, 2] = image[i, j, 2]
        resized_i += 1
    resized_i = 0
  return resized_image

#Alarga la imagen horizontales. Funcion que realiza todas las operaciones necesarias para ampliar imagenes.
def ImageEnlargeH(image, k): 
  image_original = image
  image = image[:,:,0]

  M = getMmatrixH(image) #Calculo de la matriz M
  resized_image = np.copy(image_original)
  SeamsMatrix = multipleSeamsH(M, k) #Calculo de los seams a duplicar
  Seams = SeamsMatrix

  for i in range(k):
    pos = np.argmin(SeamsMatrix[:,0]) #Seleecciona el seam situado mas arriba
    seam = np.expand_dims(SeamsMatrix[pos,:], axis=0) 
    resized_image = duplicateSeamH(resized_image, seam) #Duplica los pixel del seam
    SeamsMatrix = np.delete(SeamsMatrix, pos, axis=0) + 1 #Elimina el seam de la matriz de seam. Suma uno para
  return resized_image, Seams                             #desplazar el resto de seams porque la imagen cambia de tamaño