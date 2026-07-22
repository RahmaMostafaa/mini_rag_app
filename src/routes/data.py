from fastapi import FastAPI ,APIRouter ,Depends ,UploadFile, status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings ,Settings
from controllers import DataController, ProjectController, ProcessController
import aiofiles
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest

#Tenant
logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str ,file: UploadFile ,app_settings: Settings=Depends(get_settings)):  

    # validates the file properites
    data_controller = DataController()
    is_valid , result_signal= data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, #enum
            content={
                "signal": result_signal
            }
        )
       # if valid
    project_dir_path = ProjectController().get_project_path(project_id=project_id)

    file_path,file_id=data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
         project_id=project_id)

    try:

        async with aiofiles.open(file_path,"wb") as f:
            while chunk:= await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk) #write chunks iteratively to avoid memory overload for large files

    except Exception as e:
        #This line will shown to me as a developer in the console logs, but not to the user. The user will only see the error message in the JSON response.
        logger.error(f"Error occurred while uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value,
                "error": str(e)
            }
        )
    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id":file_id

        }
    )


@data_router.post("/process/{project_id}") # project_id : will be passed as URL but will be sent as json 
async def process_endpoint(project_id:str,process_request:ProcessRequest ):
   
    file_id=process_request.file_id
    chunk_size=process_request.chunk_size
    overlap_size=process_request.overlap_size
    
    process_controller =ProcessController(project_id=project_id)

    file_content= process_controller.get_file_content(file_id=file_id)

    file_chunks= process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )


    if file_chunks is None or len(file_chunks) == 0:

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                #In case of empty chunks
                "signal": ResponseSignal.PROCESSING_FAILED.value
            }
        )
    
    return file_chunks