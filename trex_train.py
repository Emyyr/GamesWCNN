import glob
import os
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from PIL import Image
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

imgs = glob.glob("./img_nihai/*.png") #Klasör içindeki resimleri okuma

ArithmeticError()
width = 125
height = 50

X = []
Y = []

for img in imgs: #Resimlere preprocess uygulayalım
    
    filename = os.path.basename(img)
    label = filename.split("_")[0] #Alt çizgilere göre ayırarak bir liste oluşturuyporuz
    #3 adet cloumn oluşur.
    im = np.array(Image.open(img).convert("L").resize((width, height)))
    im = im / 255
    X.append(im)    
    Y.append(label)
    
X = np.array(X)  #Traintest split içine array kabul ettiğinden array alınmalı
X = X.reshape(X.shape[0], width, height, 1) #(img , w, h , channel)

# sns.countplot(Y)

def onehot_labels(values): #Etiketleri encode ediyoruz.
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    onehot_encoder = OneHotEncoder(sparse = False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded),1) #integer encode (169,) olacağından 1 yazarak vektör haline gietiriyoruz.
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    return onehot_encoded

Y = onehot_labels(Y)
train_X, test_X, train_y, test_y = train_test_split(X, Y , test_size = 0.25, random_state = 2)    

# cnn model
model = Sequential()   
model.add(Conv2D(32, kernel_size = (3,3), activation = "relu", input_shape = (width, height, 1)))
model.add(Conv2D(64, kernel_size = (3,3), activation = "relu"))
model.add(MaxPooling2D(pool_size = (2,2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation = "relu"))
model.add(Dropout(0.4))
model.add(Dense(3, activation = "softmax"))

# if os.path.exists("./trex_weight.h5"):
#     model.load_weights("trex_weight.h5")
#     print("Weights yuklendi")    

model.compile(loss = "categorical_crossentropy", optimizer = "Adam", metrics = ["accuracy"])

model.fit(train_X, train_y, epochs = 35, batch_size = 64)

score_train = model.evaluate(train_X, train_y)
print("Eğitim doğruluğu: %",score_train[1]*100)    
    
score_test = model.evaluate(test_X, test_y)
print("Test doğruluğu: %",score_test[1]*100)      
    
open("model_new.json","w").write(model.to_json())
model.save_weights("trex_weight_new.h5")   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    