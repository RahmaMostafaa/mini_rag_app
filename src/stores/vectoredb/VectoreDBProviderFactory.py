from .VectorDBEnums import VectorDBEnums
from .providers import QdrantBDProvider
from controllers.BaseController import BaseController
class VectoreDBProviderFactory:
    
    def __init__(self, config): #config will by passed by user in (Settings)
        self.config = config

    def create(self, provider: str):
        if provider ==  VectorDBEnums.QDRANT.value:
            db_path = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)
          
            return QdrantBDProvider(
                   db_path = self.config.VECTOR_DB_PATH
                   distance_method = self.config.VECTOR_DB_DISTANCE_METHOD 
            )

        return None