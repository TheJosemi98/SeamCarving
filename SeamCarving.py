from skimage import io
import numpy as np
import scipy.signal

#Funcion que dada una imagen devuelve el seam vertical u horizontal optimo
def SeamCarving(image, VoH): #If True - Vertical, if False - Horizontal

  image = image[:,:,0]
  
  #Sobel's filter
  Gx = np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]])
  Gy = np.transpose(Gx)

  Ix = scipy.signal.convolve2d(image, Gx, mode='same')
  Iy = scipy.signal.convolve2d(image, Gy, mode='same')

  #Energy operator
  e = abs(Ix) + abs(Iy)

  if VoH:
    #Vertical Seam
    M = np.zeros(e.shape)

    for i in range(e.shape[0]): #Rows
      for j in range(e.shape[1]): #Columns

        if (i-1)>=0 and (j-1)>=0: #Condiciones frontera
          e1 = M[i-1,j-1]
        else:
          e1 = 1e20

        if (i-1)>=0: #Condiciones frontera
          e2 = M[i-1,j]
        else:
          e2 = 1e20

        if (i-1)>=0 and (j+1)<=(e.shape[1]-1): #Condiciones frontera
          e3 = M[i-1,j+1]
        else:
          e3 = 1e20

        if e1==1e20 and e2==1e20 and e3==1e20:
          M[i,j] = e[i,j]
        else:
          M[i,j] = e[i,j] + min(e1,e2,e3)

    minCost = np.argmin(M[e.shape[0]-1])

    #Removal pixel list
    pixelListV = []
    pixelListV.append((e.shape[0]-1, np.argmin(M[e.shape[0]-1])))

    i = e.shape[0]-1
    j = np.argmin(M[e.shape[0]-1])

    while i!=0:
      e1 = M[i-1, j]

      if (j-1)<0: #Condiciones frontera
        e2 = 1e20
      else:
        e2 = M[i-1, j-1]

      if (j+1)>e.shape[1]-1: #Condiciones frontera
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
    return pixelListV, minCost

  else:
    #Horizontal Seam
    M = np.zeros(e.shape)

    for j in range(e.shape[1]): #Columns
      for i in range(e.shape[0]): #Rows

        if (i-1)>=0 and (j-1)>=0: #Condiciones frontera
          e1 = M[i-1,j-1]
        else:
          e1 = 1e20

        if (j-1)>=0: #Condiciones frontera
          e2 = M[i,j-1]
        else:
          e2 = 1e20

        if (j-1)>=0 and (i+1)<=(e.shape[0]-1): #Condiciones frontera
          e3 = M[i+1,j-1]
        else:
          e3 = 1e20

        if e1==1e20 and e2==1e20 and e3==1e20: #Condiciones frontera
          M[i,j] = e[i,j]
        else:
          M[i,j] = e[i,j] + min(e1,e2,e3)

    minCost = np.argmin(M[:, e.shape[1]-1])

    #Removal pixel list
    pixelListH = []
    pixelListH.append((np.argmin(M[:,e.shape[1]-1]), e.shape[1]-1))

    i = np.argmin(M[:,e.shape[1]-1])
    j = e.shape[1]-1

    while j!=0:
      e1 = M[i, j-1]

      if (i-1)<0: #Condiciones frontera
        e2 = 1e20
      else:
        e2 = M[i-1, j-1]

      if (i+1)>e.shape[0]-1: #Condiciones frontera
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
    return pixelListH, minCost