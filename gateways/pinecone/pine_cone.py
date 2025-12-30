import os

from pinecone import Pinecone as Pinecone_lib, ServerlessSpec
from static.LogginService import LoggerService
from static.Settings import Settings
from gateways.lang_chain.lang_chain import generate_chunks
from gateways.open_ia.open_ia import OpenIaService


class PineCone:
    def __init__(self):
        settings: Settings = Settings()

        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = settings.pinecone["index_name"]
        self.region = settings.pinecone["region"]
        self.environment = settings.pinecone["environment"]
        self.metric = settings.pinecone["metric"]
        self.vector_type = settings.pinecone["vector_type"]
        self.dimension = settings.pinecone["dimension"]
        self.pinecone = Pinecone_lib(api_key=self.api_key)
        self.open_ia = OpenIaService()

        self.logger = LoggerService("PineconeService", "INFO")

    def save_user_content(self, content: str, user_code: str, company: str = '') -> None:
        if self.has_invalid_properties():
            return

        if not user_code:
            self.logger.error("User code is required to save data to Pinecone.")
            return

        try:
            chunks = generate_chunks(content)
            if not chunks:
                self.logger.info(f"No data to save for user {user_code}.")
                return

            embeddings = self.open_ia.generate_embeddings_chunks(chunks)
            if not embeddings:
                self.logger.info(f"No embeddings generated for user {user_code}.")
                return

            self.delete_vectors_by_user(user_code)
            self.create_index_if_not_exists()
            index = self.pinecone.Index(self.index_name)

            vector_insert = [
                (
                    f"{company.replace(' ','')}-{user_code}-{i}",
                    item["vector"],
                    {"text": item["text"], "user_code": user_code}
                )
                for i, item in enumerate(embeddings)
            ]

            if vector_insert:
                index.upsert(vector_insert)
                self.logger.info(f"Data saved successfully for user {user_code}.")

        except Exception as e:
            self.logger.error(f"Error saving user data to Pinecone: {e}")
            return

    def delete_vectors_by_user(self, user_code: str) -> None:
        if self.has_invalid_properties():
            return

        if not user_code:
            self.logger.error("User code is required to delete vectors.")
            return

        try:
            self.create_index_if_not_exists()
            index = self.pinecone.Index(self.index_name)
            index.delete(filter={"user_code": user_code})
            self.logger.info(f"Vectors deleted for user {user_code}.")
        except Exception as e:
            self.logger.error(f"Error deleting Pinecone vectors for user {user_code}: {e}")
            return


    def get(self, embedding, top_k=5):
        if self.has_invalid_properties():
            return None

        try:
            self.create_index_if_not_exists()
            index = self.pinecone.Index(self.index_name)

            query_response = index.query(
                vector=embedding,
                top_k=top_k,
                include_metadata=True
            )

            return query_response

        except Exception as e:
            self.logger.error(f"Error retrieving data from Pinecone: {e}")
            return []


    def create_index_if_not_exists(self) -> None:
        if not self.pinecone.has_index(self.index_name):
            try:
                self.pinecone.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric=self.metric,
                    vector_type=self.vector_type,
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=self.region
                    ),
                    deletion_protection="disabled",
                    tags={
                        "environment": self.environment,
                    }
                )
                self.logger.info(f"Index '{self.index_name}' created successfully.")
            except Exception as e:
                self.logger.error(f"Error creating index: {e}")


    def has_invalid_properties(self) -> bool:
        if self.api_key is None or self.index_name is None or self.region is None or self.environment is None or self.metric is None or self.vector_type is None:
            self.logger.error("PineCone properties are invalid")
            return True

        return False

