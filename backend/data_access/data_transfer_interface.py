import abc
import copy

from data_access.data_transfer_objects import Databases
from data_access.data_transfer_objects import Document
from data_access.data_transfer_objects import Datasets
from data_access.data_transfer_objects import DatasetDescription
class DataTransferInterface:

    @abc.abstractmethod
    def get_databases(self) -> Databases:
        pass

    @abc.abstractmethod
    def get_document(self,  database: str, collection: str, skip_count: int, query: str = "") -> Document:
        pass

    @abc.abstractmethod
    def count_documents(self, database: str, collection: str) -> int:
        pass

    @abc.abstractmethod
    def last_update_date(self, database: str, collection: str) -> str:
        pass

    @abc.abstractmethod
    def create_date(self, database: str, collection: str) -> int:
        pass


class MetadataTransferInterface:
    datasets = None

    def get_datasets_details(self) -> Datasets:
        return copy.deepcopy(self.datasets)

    def set_datasets_details(self, datasets: Datasets):
        self.datasets = datasets

    @abc.abstractmethod
    def create_dataset_description(self, dataset_description: DatasetDescription):
        pass

    @abc.abstractmethod
    def update_dataset_description(self, database: str, collection: str, number_of_documents: int, size_mb: float, created: str, last_update: str):
        pass

    @abc.abstractmethod
    def get_dataset_description(self, database: str, collection: str) -> DatasetDescription:
        pass

    @abc.abstractmethod
    def all_dataset_descriptions(self, database: str, collection: str) -> DatasetDescription:
        pass