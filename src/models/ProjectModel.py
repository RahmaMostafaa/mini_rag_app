from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    def __init__(self,db_client:object):

        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
   #First we check if this collection created or not to add index
   #in case of created we add indexes manually from 3T
   #not existed: created it from this function with indexes

# To make init + init_collection in the same time
    @classmethod
    async def create_instance(cls,db_client:object):
            instance=cls(db_client) # Because it is static.define object here it this way
            await instance.init_collection()
            return instance

    async def init_collection(self):
      all_collection =await self.db_client.list_collection_names()
      if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collection:
        self.collection =self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
        indexes= Project.get_indexes()
        for index in indexes:
            await self.collection.create_index(
                index["key"],
                name=index["name"],
                unique=index["unique"]
            ) # So here separate logic of index from implementation



    #Insert# a project into MongoDB.
    async def create_project(self, project: Project):
        #solve (_id) problem => (by_alias=True,exclude_inset=True)
        result=await self.collection.insert_one(project.dict(by_alias=True,exclude_unset=True))
        project._id=result.inserted_id

        return project

    async def get_project_or_create_one(self, project_id: str):

    #Find# the project in the collection by project_id
        record= await self.collection.find_one({
            "project_id": project_id

        })

        if record is None:

            #create new project
            project = Project(project_id=project_id)
            project = await self.create_project(project=project)

            return project

        return Project(**record)

    async def get_all_projects(self,page:int=1, page_size:int=10):
       
        #count total documents in the collection
        total_documents= await self.collection.count_documents({})

        total_pages = total_documents// page_size
        if total_documents % page_size > 0:
            total_pages += 1

        cursor =  self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects=[]
        async for document in cursor:
            projects.append(Project(**document))

            return projects, total_pages


