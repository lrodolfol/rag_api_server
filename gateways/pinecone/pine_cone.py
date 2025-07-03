import os

from pinecone import Pinecone as Pinecone_lib, ServerlessSpec
from static.LogginService import LoggerService
from static.Settings import Settings


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

        self.logger = LoggerService("PineconeService", "INFO")


    def save(self, embeddings) -> None:
        if self.has_invalid_properties():
            return

        try:
            self.create_index_if_not_exists()
            index = self.pinecone.Index(self.index_name)

            vector_insert = [(
                    f"id-{i}",  # ID único
                    item["vector"],
                    {"text": item["text"]}  # metadado
                )
                for i, item in enumerate(embeddings)
            ]

            index.upsert(vector_insert)
            self.logger.info("Data saved successfully with pinecone.")

        except Exception as e:
            self.logger.error(f"Error initializing Pinecone: {e}")
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
