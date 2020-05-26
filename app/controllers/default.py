from app import app, db
from app.models.models import UploadImage
from flask import request
from base64 import b64decode, b64encode
from app.tf_model.model import unet_256
from numpy import fromstring, uint8, array, squeeze, float32
from cv2 import imdecode, resize, IMREAD_UNCHANGED, INTER_CUBIC, imencode

model = unet_256()
model.load_weights('./app/tf_model/best_weights_17.hdf5')

# routes is here

@app.route("/predict", methods=['POST', 'GET'])
def predict():
    if request.method == "POST":
        try:
            imgb64 = request.data['arquivo']
            img = fromstring(b64decode(imgb64), uint8)
            img = imdecode(img, IMREAD_UNCHANGED)
            img = resize(img, (625, 352))
            img = img[39:336, ]
            img = resize(img, (256, 256), interpolation=INTER_CUBIC)
            img = img.reshape((1,) + img.shape)
            img = array(img, float32) / 255

            pred = model.predict_on_batch(img)
            pred = squeeze(pred, axis=3)
            pred = array(pred, float32) * 255
            pred = pred.transpose(1, 0, 2).reshape(-1, pred.shape[1])

            pred = resize(pred, (512, 256))
            _, pred = imencode('.png', pred)
            pred = pred.tobytes()
            pred_b64 = b64encode(pred)

            new_file = UploadImage(imgb64.encode(), pred_b64)
            db.session.add(new_file)
            db.session.commit()

            return {
                'dataDeEnvio' : request.data['dataDeEnvio'],
                'nomeArquivo' : request.data['nomeArquivo'],
                'predict': pred_b64.decode('utf-8')
            }
        except:
                return {'message': 'Run-time error' }


    return {'url': request.url}