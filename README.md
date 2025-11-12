# 🎨 Van Gogh Art Studio

[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.7-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

Transform your photos into stunning Van Gogh-style masterpieces using deep learning and neural style transfer. Experience the magic of AI art generation with just one click!

![Van Gogh Art Studio Demo](static/demo.png)

<div align="center">
  <table>
    <tr>
      <td align="center"><strong>Content</strong></td>
      <td align="center"><strong>Style</strong></td>
      <td align="center"><strong>Result</strong></td>
    </tr>
    <tr>
      <td align="center">
        <img src="examples/content/mountain.jpg" style="width: 400px; height: 350px; object-fit: cover; border-radius: 8px;" alt="Original Mountain">
        <br>
      </td>
      <td align="center">
        <img src="examples/style/van_gogh/wheatfield_with_crows.jpg" style="width: 400px; height: 350px; object-fit: cover; border-radius: 8px;" alt="Wheatfield Style">
        <br>
      </td>
      <td align="center">
        <img src="static/result_demo.jpg" style="width: 400px; height: 350px; object-fit: cover; border-radius: 8px;" alt="Van Gogh Result">
        <br>
      </td>
    </tr>
  </table>
</div>

## ✨ Features

- 🎨 **10+ Van Gogh Styles** - Starry Night, Sunflowers, Almond Blossom, and more
- 🖼️ **Easy Upload** - Drag & drop interface for seamless photo upload
- ⚡ **Real-time Processing** - Watch as your photo transforms in real-time
- 📱 **Responsive Design** - Works perfectly on desktop and mobile
- 💾 **Instant Download** - Download high-resolution artwork instantly
- 🐳 **Docker Powered** - One-command deployment, no setup required

## 🚀 Quick Start

### Run with Docker (Recommended)

```bash
docker run -p 8000:8000 trongkhanh083/van-gogh-studio
```

## 🛠️ For Developers

### Clone the repository
```
git clone https://github.com/trongkhanh083/neural-style-transfer.git
cd neural-style-transfer
```
### Create conda environment
```
conda create -n fast-nst tensorflow-gpu==2.1.0
conda activate fast-nst
```

### Install dependencies
```
pip install -r requirements.txt
```

### Run the application
```
python main.py
```
### Build the image
```
docker build -t van-gogh-studio .
```

### Run locally built image
```
docker run -p 8000:8000 van-gogh-studio
```

## 📝 License
  - This project is licensed under the MIT License.

## 🙏 Acknowledgments
  - Van Gogh's artwork for the incredible inspiration
  - FastAPI for the robust web framework
  - Docker for seamless deployment
  - The open-source community for various AI/ML libraries
