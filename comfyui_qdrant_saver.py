from qdrant_client import QdrantClient
from qdrant_client.http.models import CollectionStatus, PointStruct


class QDrantSaver:
    RETURN_TYPES = ("STRING",)  # Đặt RETURN_TYPES thành thuộc tính lớp
    FUNCTION = "save"
    CATEGORY = "QDrant"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "id": ("CONDITIONING",),
                "title": ("CONDITIONING",),
                "link": ("CONDITIONING",),
                "vector": ("VECTOR",),
                "markdown": ("CONDITIONING",),
                "metadata": ("CONDITIONING",),
                "qdrant_endpoint": ("STRING", {
                    "multiline": False,
                    "default": "http://localhost:6333",
                    "lazy": True
                }),
                "collection_name": ("STRING", {
                    "multiline": False,
                    "default": "default_collection",
                    "lazy": True
                }),
                "print_to_screen": (["enable", "disable"],),
            },
        }

    def check_lazy_status(self, qdrant_endpoint, print_to_screen):
        if print_to_screen == "enable":
            return ["qdrant_endpoint", "collection_name"]
        else:
            return []

    def save(self, id, title, link, vector, markdown, metadata, qdrant_endpoint, collection_name, print_to_screen):
        client = QdrantClient(qdrant_endpoint)
        collections = client.get_collections()
        if not any(collection_name == c.name for c in collections.collections):
            client.create_collection(collection_name)
        collection = client.get_collection(collection_name)
        if collection.status != CollectionStatus.Active:
            client.activate_collection(collection_name)
        _point = PointStruct(id=id, vector=vector, payload={**metadata, "title": title, "link": link, "markdown": markdown})
        client.insert(collection_name, [_point])
        return (f"Saved {title} to {collection_name}",)
