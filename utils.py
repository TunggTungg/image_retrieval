import tritonclient.grpc as grpc_client
from tritonclient.grpc import InferenceServerClient
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
import cv2,  base64

def convert_img(encoded_img):
    if isinstance(encoded_img, str):
        b64_decoded_image = base64.b64decode(encoded_img)
    else:
        b64_decoded_image = encoded_img

    img_arr = np.fromstring(b64_decoded_image, np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    img = np.expand_dims(img,axis=0).astype(np.float32)
    img = preprocess_input(img)
    return img

def grpc_infer(img):
	triton_client = InferenceServerClient(url='10.5.0.5:8001')
	img = convert_img(img)
	test_input = grpc_client.InferInput("input_1", img.shape, datatype="FP32")
	test_input.set_data_from_numpy(img)

	try:
		test_output = grpc_client.InferRequestedOutput("avg_pool")
		results = triton_client.infer(model_name="resnet50", inputs=[test_input], outputs=[test_output])
		output_array = results.as_numpy('avg_pool')
		return output_array
	except Exception as e:
		print(e)
		return None

if __name__ == '__main__':
	image = cv2.imread('test.jpg')
	input_image  = cv2.resize(image, (224,224))
	input_image = np.expand_dims(input_image,axis=0).astype(np.float32)
	triton_client = InferenceServerClient(url='localhost:8001')
	test_input = grpc_client.InferInput("input_1", input_image.shape, datatype="FP32")
	test_input.set_data_from_numpy(input_image)

	test_output = grpc_client.InferRequestedOutput("avg_pool")

	results = triton_client.infer(model_name="resnet50", inputs=[test_input], outputs=[test_output])
	output_array = results.as_numpy('avg_pool')
	print(output_array)
