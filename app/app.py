import base64
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
import pickle
from utils import grpc_infer
import imghdr

# Load Data
path = np.load('./features/all_feartures_trt.npz')['path']

# Load LCPO
with open('./features/index.pkl', 'rb') as inp:
    loaded_index = pickle.load(inp)

# Init FastAPI
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
def is_valid_image_extension(filename: str) -> bool:
	ext = filename.split(".")[-1]
	return ext.lower() in ALLOWED_IMAGE_EXTENSIONS

def is_valid_image_content(file: bytes) -> bool:
	return imghdr.what(None, h=file) in ALLOWED_IMAGE_EXTENSIONS

@app.get("/")
async def homepage(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(request: Request, file: UploadFile = File(...)):
	# Check if the filename has a valid image extension
	if not is_valid_image_extension(file.filename):
		raise HTTPException(status_code=400, detail="Only image files are allowed")

	# Read the content of the uploaded file
	input_image_data = await file.read()

	# Check if the content is a valid image
	if not is_valid_image_content(input_image_data):
		raise HTTPException(status_code=400, detail="Invalid image file")
	
	input_image_base64 = base64.b64encode(input_image_data).decode('utf-8')

	feature = grpc_infer(input_image_data)
	loaded_index.nprobe = 10            # make comparable with experiment above
	D, I = loaded_index.search(feature, 30)# search
	result_list = [path[i] for i in I[0]]
	return templates.TemplateResponse("index.html", {"request": request, "input_img":f'data:image/jpeg;base64,{input_image_base64}', \
												  	 "result_list":result_list})
