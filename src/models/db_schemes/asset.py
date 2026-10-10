from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class Asset(BaseModel):

        id: Optional[ObjectId]= Field(None ,alias="_id")
        asset_project_id: ObjectId
        asset_type: str =Field(...,min_length=1) #file, URL, SQL connection..etc
        asset_name: str =Field(...,min_length=1) #file_id in this case
        asset_size: int = Field(ge=0, default=None) #bytes of file, not file=> not important
        asset_config: dict = Field(default=None)
        asset_pushed_at: datetime = Field(default=datetime.utcnow)   #Time that asset created at database

        class Config: # TO Handle ObjectId errors
           arbitrary_types_allowed=True 


        #for indexing
        @classmethod
        def get_indexes(cls):#static

            return [
                {
                    "key":[
                        ("asset_project_id",1) #1=>accending , -1=> decesending
                    ],
                    "name": "asset_project_id_index_1",
                    "unique": False
                },
                {
                    "key":[
                        ("asset_project_id",1),
                        ("asset_name",1) 
                    ],
                    "name": "asset_project_id_name_index_1",
                    "unique": True
                }
            ]