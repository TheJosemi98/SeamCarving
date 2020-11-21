from skimage.transform import resize
from reduceSC import reduceSC

#Función especifica que aplica una amplificación del contenido a un imagen especifica. Según una cantidad determinada, se aumenta 
#la resolución tanto en columnas como en filas, y luego posteriomente se aplica el metodo Seam Carving hasta alcanzar la misma resolución
#de la imagen inicial
def contentAmplification(image, dimResolution):

  img_ampl = resize(image,(image.shape[0]+dimResolution,image.shape[1]+dimResolution), anti_aliasing = True)
  image_resultado = reduceSC(img_ampl,(image.shape[0], image.shape[1]))

  return image_resultado