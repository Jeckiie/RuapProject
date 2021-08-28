from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
import numpy as np
import pandas as pd
import os, os.path

model = VGG16(weights='imagenet', include_top=True)
#model.summary()

#df_final = pd.DataFrame()
#images = []
valid_images = ['.jpg', '.png']
pathNames = ['Breskva', 'Grab', 'Jabuka', 'Kruska', 'Visnja']
df_final = pd.DataFrame()
for path in pathNames:
    images = []
    for files in os.listdir('./' + path):
        ext = os.path.splitext(files)[1]
        if ext.lower() not in valid_images:
            continue
        img = image.load_img(os.path.join('./' + path, files), target_size=(224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)
        vgg16_feature = model.predict(img_data)
        row_to_add = pd.DataFrame(vgg16_feature)
        row_to_add.insert(0, "Name", path, True)
        df_final = df_final.append(row_to_add, ignore_index=True)
    #df_final.to_csv(path + '.csv', index_label='id')
#df_final.to_csv('leaf_train.csv', index_label='id')
df_final.to_csv('leaf_train_dataset.csv', index=False)
'''
path = './images'
valid_images = ['.jpg', '.png']
for files in os.listdir(path):
    ext = os.path.splitext(files)[1]
    if ext.lower() not in valid_images:
        continue
    #images.append(Image.open(os.path.join(path, files)))
    img = image.load_img(os.path.join(path, files), target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    vgg16_feature = model.predict(img_data)
    #final_array = np.array([os.path.splitext(files)[0]])
    #final_array = np.append(final_array, vgg16_feature)
    #row_to_add = pd.DataFrame(vgg16_feature)
    row_to_add = pd.DataFrame(vgg16_feature)
    #row_to_add = row_to_add.insert(loc=0, column='name', value='xd')
    #ignore_index = True, da poveća id za 1
    df_final = df_final.append(row_to_add, ignore_index=True)
    
#df_final = pd.DataFrame()
df_final.to_excel('excelFinal.xlsx', index_label='id')
'''


'''
for imageFile in images:
    img = image.load_img(imageFile, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    vgg16_feature = model.predict(img_data)
    row_to_add = pd.DataFrame(vgg16_feature)
    df_final = df_final.append(row_to_add)
'''

'''
img_path= './acer_opalus.jpg'
img = image.load_img(img_path, target_size=(224, 224))
img_data = image.img_to_array(img)
img_data = np.expand_dims(img_data, axis=0)
img_data = preprocess_input(img_data)

vgg16_feature = model.predict(img_data)
#np.savetxt('features.txt', vgg16_feature)
df = pd.DataFrame(vgg16_feature)
df.to_excel('excelFile.xlsx', index_label='id')
'''

