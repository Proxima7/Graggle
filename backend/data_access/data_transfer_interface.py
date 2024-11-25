import abc
import copy

from data_access.data_transfer_objects import Databases
from data_access.data_transfer_objects import Document
from data_access.data_transfer_objects import Datasets
from data_access.data_transfer_objects import DatasetDescription
from data_access.data_transfer_objects import Bookmarkgroups

class UserSessionInterface:
    """
    Interface for a user session

    Domain: Data direct linked to the SSO user
    """

    @abc.abstractmethod
    def get_username(self) -> str:
        """
        Interface to get username

        Returns: username

        """
        pass

    @abc.abstractmethod
    def get_bookmark_groups(self) -> Bookmarkgroups:
        """
        Interface to get Bookmarkgroups of user

        Returns: Bookmarkgroups

        """
        pass

    @abc.abstractmethod
    def set_bookmark_groups(self) -> Bookmarkgroups:
        """
        Interface to set Bookmarkgroups of user

        Returns: Bookmarkgroups

        """
        pass

class DataTransferInterface:
    """
    Interface for a custom data storage implementation.

    Domain: Data of the real documents

    Database needs to be seen as the equivalent of your storage solution.
    Collection needs to be ssen as the equivalent of your storage solution (e.g. table for relational databases).

    """

    @abc.abstractmethod
    def get_databases(self) -> Databases:
        """
        Get the full list of datbases and there collections.

        Returns: List that contains all necessary databases and collections
        """
        pass

    @abc.abstractmethod
    def get_document(self,  database: str, collection: str, skip_count: int, query: str = "") -> Document:
        """
        Get a single document from the data storage by the given parameter.

        Args:
            database: database name
            collection: collection name
            skip_count: number of documents to skip
            query: filter query for the document collection (mongodb query style)

        Returns: filtered document
        """
        pass

    @abc.abstractmethod
    def count_documents(self, database: str, collection: str) -> int:
        """
        Number of documents in the collection of the database.

        Args:
            database: database name
            collection: collection name

        Returns: Total number of documents in the collection

        """
        pass

    @abc.abstractmethod
    def last_update_date(self, database: str, collection: str) -> str:
        """
        Date with time when the collection was last updated.

        Args:
            database: database name
            collection: collection name

        Returns: Daten with time in human readable format when the collection was last updated
        """
        pass

    @abc.abstractmethod
    def create_date(self, database: str, collection: str) -> int:
        pass


class MetadataTransferInterface:
    """
    Interface for a custom data storage implementation.

    Domain: Metadate of the documents to understand ad classify the documents
    """

    datasets = None

    def get_datasets_details(self) -> Datasets:
        """Deepcopy of the datasets"""
        return copy.deepcopy(self.datasets)

    def set_datasets_details(self, datasets: Datasets):
        """Set the datasets to the class variable"""
        self.datasets = datasets

    @abc.abstractmethod
    def insert_dataset_description(self, dataset_description: DatasetDescription) -> list[str]:
        """
        Insert a new dataset description into the data storage.

        Args:
            dataset_description: dataset description to add

        Returns: list of id of inserted document
        """
        pass

    @abc.abstractmethod
    def update_dataset_description(self, database: str, collection: str, number_of_documents: int, size_mb: float, created: str, last_update: str):
        """
        Update of certain values of the dataset description.
        Args:
            database: database name
            collection: collection name
            number_of_documents: replacing value of number_of_documents in collection
            size_mb: replacing value of size_mb of all images in storage
            created: replacing value of created time and date human readable
            last_update: replacing value of last_update time and date human readable
        """
        pass

    @abc.abstractmethod
    def get_dataset_description(self, database: str, collection: str) -> DatasetDescription:
        """
        Get the dataset description complete.

        Args:
            database: database name
            collection: collection name

        Returns: Dataset description object

        """
        pass

    @abc.abstractmethod
    def all_dataset_descriptions(self) -> DatasetDescription:
        """
        Get all dataset description at one time.

        Returns: all possible Dataset description objects

        """
        pass