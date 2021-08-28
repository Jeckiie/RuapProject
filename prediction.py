import urllib.request
import json
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from .models import Image
import numpy as np
import pandas as pd
import re

def getPrediction(filename):
    model = VGG16(weights='imagenet', include_top=True)
    img = Image.query.filter_by(path='/static/' + filename).first()
    if not img:
        return 'can not find image with that name', 404
    imagePath = ".." + img.path;
    img = image.load_img(imagePath, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    vgg16_feature = model.predict(img_data)
    df = pd.DataFrame(vgg16_feature)
    df.index.name = 'id'

    jsonData = df.reset_index().to_dict(orient='records')

    for elem in jsonData:
        for x in elem:
            elem[x] = str(elem[x])

    data2 = {
            "Inputs": {
                "input1": jsonData,
            },
            "GlobalParameters": {
            }
    }

    body = str.encode(json.dumps(data2))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/113ea050dcd64e97b75c318115b6ad19/services/7f114e6d98da4da485199db749967a53/execute?api-version=2.0&format=swagger'
    api_key = 'JXtMEv5XQF1bX/2u6o1uMxQyXLmb5Kz8rfpuOBRHdlzi0qvNvn3/UenJzCYhPShoPcwSv5IsfDPk3ZJ9YTGVmg==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)
    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        result = str(result)
        result = result.replace('b\'{"Results":{"output1":[{"Scored Probabilities for Class \\\\', "")
        result = result.replace('\\""', "")
        result = result.replace(',"Scored Probabilities for Class \\\\"', "")
        result = result.replace('\\', "")
        result = result.replace('}]}}', "")
        breskva = float(re.search('"Breskva:"(.+?)"Grab:"', result).group(1))
        grab = float(re.search('"Grab:"(.+?)"Jabuka:"', result).group(1))
        jabuka = float(re.search('"Jabuka:"(.+?)"Kruska:"', result).group(1))
        kruska = float(re.search('"Kruska:"(.+?)"Visnja:"', result).group(1))
        visnja = float(re.search('"Visnja:"(.+?)","Scored Labels"', result).group(1))
        highest = max(breskva, grab, jabuka, kruska, visnja)
        label = re.search('"Scored Labels":"(.+?)"', result).group(1)
        percentage = str(round(highest * 100, 5) )
        prediction = label + ": " + percentage + "%"
        print(prediction)
        return prediction
        #result = result[0][0]
        #return result[1], result[2]*100
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        #print(json.loads(error.read().decode("utf8", 'ignore')))
        result = json.loads(error.read().decode("utf8", 'ignore'))

        print(result)
        return result
#    label = decode_predictions(vgg16_feature)
#    label = label[0][0]
#    print('%s (%.2f%%)' % (label[1], label[2]*100))
#    return label[1], label[2]*100

#getPrediction('iPAD2_C32_EX01.jpg');
