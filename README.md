
# **Image Retrieval**

## Demo video
<p align="center">
  <img src="demo/video.gif"><br/>
  <i>Project deployment.</i>
</p>

## Description
This project aims to build an image retrieval system that utilizes deep learning [ResNet](https://keras.io/api/applications/resnet/) for feature extraction, [Local Optimized Product Quantization](https://github.com/facebookresearch/faiss) techniques for storage and retrieval, and efficient deployment using Nvidia technologies like [TensorRT](https://developer.nvidia.com/tensorrt) and [Triton Server](https://developer.nvidia.com/triton-inference-server), all accessible through a [FastAPI](https://fastapi.tiangolo.com/)-powered web API.

## Run Locally

Clone the project

```bash
  git clone https://github.com/TunggTungg/image_retrieval.git
```

Go to the project directory

```bash
  cd image_retrieval
```

Run with Docker

```bash
  docker-compose up --build
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)