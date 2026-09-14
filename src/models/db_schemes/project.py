from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId


class Project(BaseModel):
    id:Optional[ObjectId]= Field(None ,alias="_id") #In Python, call this field id, but when communicating with MongoDB/data dictionaries, treat it as _id
    project_id:str = Field(...,min_length=1)

    @validator('project_id')
    def validate_project_id(cls,value): #class of the project

        if not value.isalnum():
            raise ValueError('Project_id must be Alphanumeric')

        return value

    class Config: # TO Handle ObjectId errors
        arbitrary_types_allowed=True 