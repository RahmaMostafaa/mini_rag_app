from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel): #class for end points requests

    file_id:str
    chunk_size :Optional[int]=100
    overlap_size:Optional[int]=20
    do_reset:Optional[int]=0 # deal with bool in form of (0,1) instead of (True or False)+ this action from user
