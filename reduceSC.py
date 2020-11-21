from SeamCarving import SeamCarving
from removePixels import removePixels

#Funcion que calcula el seam optimo y lo elimina de la imagen original. Como entrada tiene la imagen original y una 
#variable booleana para determinar si lo hace por seams verticales u horizontales. True - vertical, False - horizontal
def SeamCarvingBase(image, VoH):
    pixelList, minCost = SeamCarving(image, VoH)
    image = removePixels(image, pixelList, VoH)
    return image

#Esta funcion se encargar de reducir una imagen a una resolucion deseado. Como entrada tiene la imagen original y
#la resolucion deseada. Como salida devuelve la imagen con la resolucion introducida.

def reduceSC(image, final_resolution):
    row_final, col_final = final_resolution
    row_ini, col_ini = image.shape[0], image.shape[1]

    if (((row_ini - row_final) < 0) or ((col_ini - col_final) < 0)): #Comprobacion de la resolucion
        print('Incorrect target resolution')
    else:
        step_row = row_ini - row_final
        step_col = col_ini - col_final

        if (step_row <= step_col):
            diff = step_col - step_row
            z = 1
        else:
            diff = step_row - step_col
            z = 0

        n_iter = step_row + step_col - diff

        VoH = True
        for i in range(n_iter): #Realiza de forma alternada la eliminacion de seams verticales y horizontales
            image = SeamCarvingBase(image, VoH)
            VoH = not VoH

        if (z == 1):
            for i in range(diff):
                image = SeamCarvingBase(image, True)
        else:
            for i in range(diff):
                image = SeamCarvingBase(image, False)

    return image

