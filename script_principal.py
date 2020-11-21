from skimage import io
import matplotlib.pyplot as plt
import numpy as np

from reduceSC import reduceSC
from enlargeSC import enlargeSC
from draw_roi import draw_roi
from ContentAmplification import contentAmplification
from objectRemoval import objectRemoval

#%% Cargar imagenes
example_id = 'example_10'
PATH = 'examples/'
PATH += example_id + '.png'

image = io.imread(PATH)/255.0

if len(image.shape)<3:
  image = np.stack((image,image,image),axis=2)

print(image.shape)
plt.figure(1)
plt.title('Imagen inicial')
plt.imshow(image)

#%% Reducir tamaño de la imagen
final_size = (720, 450) #Resolucion deseada
resized_image = reduceSC(image, final_size)
plt.figure(2)
plt.title('Imagen reducida a ('+str(final_size[0])+' , '+str(final_size[1])+')')
plt.imshow(resized_image)
io.imsave("resultados/resultado.png", resized_image)
print(resized_image.shape)

#%% Aumentar tamaño de la imagen
final_size = (750, 490) #Resolucion deseada
resized_image = enlargeSC(image[:,:,0:3], final_size)
plt.figure(3)
plt.title('Imagen aumentada a ('+str(final_size[0])+' , '+str(final_size[1])+')')
plt.imshow(resized_image)
io.imsave("resultados/resultado.png", resized_image)
print(resized_image.shape)

#%% Amplificacion de contenido
image_resultado = contentAmplification(image, 50)

plt.figure(4)
plt.title('Imagen resultado de la amplificación')
plt.imshow(image_resultado)

# Eliminacion de objetos #

#%% Dibujar ROI
ROI = [330, 355, 70, 50] #ROI deseada - [x, y, alto, ancho]
image_roi = draw_roi(image, ROI)
plt.figure(5)
plt.title('Imagen con ROI señalada')
plt.imshow(image_roi)

#%% Eliminar objeto seleccionado
image_resultado = objectRemoval(image, ROI)
plt.figure(6)
plt.title('Imagen resultado de la eliminación de objetos')
plt.imshow(image_resultado)