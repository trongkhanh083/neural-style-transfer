from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Form
from fastapi.responses import Response, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import uuid
import uvicorn
import os
import io
from PIL import Image

app = FastAPI(
    title="Neural Style Transfer API",
    description="Transform your photos into Van Gogh artwork",
    version="1.0.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/examples", StaticFiles(directory="examples"), name="examples")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configuration
VAN_GOGH_STYLES = {
    "almond_blossom": {
        "name": "Almond Blossom",
        "preview": "/examples/style/van_gogh/almond_blossom.jpg"
    },
    "cafe_terrace": {
        "name": "Café Terrace at Night", 
        "preview": "/examples/style/van_gogh/cafe_terrace_at_night.jpg"
    },
    "irises": {
        "name": "Irises",
        "preview": "/examples/style/van_gogh/irises.jpg"
    },
    "self_portrait": {
        "name": "Self Portrait with Bandaged Ear",
        "preview": "/examples/style/van_gogh/self-portrait_with_bandaged_ear.jpg"
    },
    "starry_night": {
        "name": "Starry Night",
        "preview": "/examples/style/van_gogh/starry_night.jpg"
    },
    "starry_night_over_rhone": {
        "name": "Starry Night Over the Rhone",
        "preview": "/examples/style/van_gogh/starry_night_over_the_rhone.jpg"
    },
    "sunflowers": {
        "name": "Sunflowers",
        "preview": "/examples/style/van_gogh/sunflowers.jpg"
    },
    "the_bedroom": {
        "name": "The Bedroom",
        "preview": "/examples/style/van_gogh/the_bedroom.jpg"
    },
    "the_potato_eaters": {
        "name": "The Potato Eaters",
        "preview": "/examples/style/van_gogh/the_potato_eaters.jpg"
    },
    "wheatfield_with_crows": {
        "name": "Wheatfield with Crows",
        "preview": "/examples/style/van_gogh/wheatfield_with_crows.jpg"
    }
}

VAN_GOGH_CKPT = {
    "almond_blossom": "checkpoints/van_gogh/almond_blossom",
    "cafe_terrace": "checkpoints/van_gogh/cafe_terrace_at_night",
    "irises": "checkpoints/van_gogh/irises",
    "self_portrait": "checkpoints/van_gogh/self-portrait_with_bandaged_ear",
    "starry_night": "checkpoints/van_gogh/starry_night",
    "starry_night_over_rhone": "checkpoints/van_gogh/starry_night_over_the_rhone",
    "sunflowers": "checkpoints/van_gogh/sunflowers",
    "the_bedroom": "checkpoints/van_gogh/the_bedroom",
    "the_potato_eaters": "checkpoints/van_gogh/the_potato_eaters",
    "wheatfield_with_crows": "checkpoints/van_gogh/wheatfield_with_crows"
}

image_cache = {}

def apply_style_transfer_sync(input_images_bytes: bytes, style: str) -> bytes:
    try:
        job_id = str(uuid.uuid4())

        input_path = f"/tmp/{job_id}_input.jpg"
        output_path = f"/tmp/{job_id}_output.jpg"

        with open(input_path, 'wb') as f:
            f.write(input_images_bytes)

        checkpoint_path = VAN_GOGH_CKPT.get(style, VAN_GOGH_CKPT["starry_night"])

        cmd = [
            'python', 'inference.py',
            '--checkpoint', checkpoint_path,
            '--in-path', input_path,
            '--out-path', output_path,
            '--allow-different-dimensions'
        ]

        results = subprocess.run(
            cmd, 
            capture_output=True,
            text=True,
            timeout=120
        )

        if results.returncode == 0 and os.path.exists(output_path):
            with open(output_path, 'rb') as f:
                output_bytes = f.read()

            try:
                os.remove(input_path)
                os.remove(output_path)
            except:
                pass

            return output_bytes
        else:
            raise Exception(f"Style transfer failed: {results.stderr}")

    except Exception as e:
        try:
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
        except:
            pass
        raise e

def process_image_background(job_id: str, input_images_bytes: bytes, style: str):
    try:
        result_bytes = apply_style_transfer_sync(input_images_bytes, style)

        image_cache[job_id]["result"] = result_bytes
        image_cache[job_id]["status"] = "completed"
        image_cache[job_id]["message"] = f"{VAN_GOGH_STYLES[style]['name']} style applied successfully"

    except Exception as e:
        image_cache[job_id]["status"] = "error"
        image_cache[job_id]["message"] = f"Processing failed: {str(e)}"


# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return templates.TemplateResponse("index.html", {"request": {}, "styles": VAN_GOGH_STYLES})

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Van Gogh Style Transfer",
        "available_styles": list(VAN_GOGH_STYLES.keys())
    }

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/icons8-artist-16.png")

@app.post("/process/")
async def process_image(background_tasks: BackgroundTasks, file: UploadFile = File(...), style: str = Form("starry_night")):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    if style not in VAN_GOGH_STYLES:
        raise HTTPException(status_code=400, detail=f"Invalid style. Available styles: {list(VAN_GOGH_STYLES.keys())}")
    
    input_images_bytes = await file.read()

    job_id = str(uuid.uuid4())

    image_cache[job_id] = {
        "original": input_images_bytes,
        "style": style,
        "status": "processing"
    }

    background_tasks.add_task(
        process_image_background,
        job_id,
        input_images_bytes,
        style
    )

    return {
        "job_id": job_id,
        "status": "processing",
        "message": f"Applying {VAN_GOGH_STYLES[style]['name']} style...",
        "style": style,
        "preview_url": f"/preview/{job_id}",
        "original_url": f"/original/{job_id}",
        "result_url": f"/result/{job_id}"
    }

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in image_cache:
        raise HTTPException(status_code=404, detail="Job not found")
    
    cache_data = image_cache[job_id]

    if cache_data["status"] == "completed":
        return {
            "job_id": job_id,
            "status": "completed",
            "message": cache_data["message"],
            "style": cache_data["style"],
            "preview_url": f"/preview/{job_id}",
            "original_url": f"/original/{job_id}",
            "result_url": f"/result/{job_id}",
            "download_url": f"/download/{job_id}"
        }
    elif cache_data["status"] == "error":
        return {
            "job_id": job_id,
            "status": "error",
            "message": cache_data["message"]
        }
    else:
        return {
            "job_id": job_id,
            "status": "processing",
            "message": f"Applying {VAN_GOGH_STYLES[cache_data['style']]['name']} style..."
        }
    
@app.get("/original/{job_id}")
async def get_original_image(job_id: str):
    if job_id not in image_cache or "original" not in image_cache[job_id]:
        raise HTTPException(status_code=404, detail="Original image not found")
    
    image_bytes = image_cache[job_id]["original"]

    return Response(
        content = image_bytes,
        media_type="image/jpeg"
    )

@app.get("/result/{job_id}")
async def get_result_image(job_id: str):
    if job_id not in image_cache or image_cache[job_id]["status"] != "completed":
        raise HTTPException(status_code=404, detail="Result image not found or not completed")
    
    image_bytes = image_cache[job_id]["result"]

    return Response(
        content = image_bytes,
        media_type="image/jpeg"
    )

@app.get("/preview/{job_id}")
async def get_preview_image(job_id: str, width: int = 1200, height: int = 950):
    if job_id not in image_cache or "result" not in image_cache[job_id]:
        raise HTTPException(status_code=404, detail="Preview not found")
    
    image_bytes = image_cache[job_id]["result"]
    image = Image.open(io.BytesIO(image_bytes))

    image.thumbnail((width, height))

    output = io.BytesIO()
    image.save(output, format="JPEG", quality=85)
    output_bytes = output.getvalue()

    return Response(
        content = output_bytes,
        media_type="image/jpeg"
    )

@app.get("/download/{job_id}")
async def download_result(job_id:str):
    if job_id not in image_cache or image_cache[job_id]["status"] != "completed":
        raise HTTPException(status_code=404, detail="Job not found or not completed")
    
    image_bytes = image_cache[job_id]["result"]
    style = image_cache[job_id]["style"]
    filename = f"van_gogh_{style}_{job_id[:8]}.jpg"
    
    return Response(
        content = image_bytes,
        media_type="image/jpeg",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/styles")
async def get_available_styles():
    return {
        "available_styles": VAN_GOGH_STYLES,
        "checkpoints": VAN_GOGH_CKPT
    }

@app.on_event("startup")
async def startup_event():
    pass
    
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1
    )
