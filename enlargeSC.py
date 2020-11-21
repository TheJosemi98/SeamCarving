from ImageEnlargeH import ImageEnlargeH
from ImageEnlargeV import ImageEnlargeV

#Esta funcion se encargar de alargar una imagen a un tamaño deseado. Como entrada tiene la imagen original y
#la resolucion deseada. Como salida devuelve la imagen con la resolucion introducida.

def enlargeSC(image, final_resolution):
  row_final, col_final = final_resolution
  row_ini, col_ini = image.shape[0], image.shape[1]

  if (((row_ini - row_final) > 0) or ((col_ini - col_final) > 0)):
    print('Incorrect target resolution') #Comprobacion sobre las dimensiones. Deben ser mayores o iguales a las originales
  else:
    if ((row_ini - row_final) != 0): #Siempre y cuando se exija un alargamiento en dicha dimension
      resized_image, _ = ImageEnlargeH(image, row_final-row_ini) #Realiza el alargamiento mediante seams horizontales
    else:                                                        #Alargamiento vertical.
      resized_image = image
      
    if ((col_ini - col_final) != 0): #Siempre y cuando se exija un alargamiento en dicha dimension
      resized_image_target, _ = ImageEnlargeV(resized_image, col_final-col_ini) #Realiza el alargamiento mediante
    else:                                                                       #seams verticales. Alargamiento horizontal.
      resized_image_target = resized_image

    return resized_image_target