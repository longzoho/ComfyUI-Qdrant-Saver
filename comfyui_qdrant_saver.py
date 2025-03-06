from qdrant_client import QdrantClient
from qdrant_client.http.models import CollectionStatus


class QDrantSaver:
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
                "metadata": ("CONDITIONING",),
                "qdrant_endpoint": ("STRING", {
                    "multiline": False,  # True if you want the field to look like the one on the ClipTextEncode node
                    "default": "http://localhost:6333",
                    "lazy": True
                }),
                "collection_name": ("STRING", {
                    "multiline": False,  # True if you want the field to look like the one on the ClipTextEncode node
                    "default": "default_collection",
                    "lazy": True
                }),
                "print_to_screen": (["enable", "disable"],),
            },
        }

        RETURN_TYPES = ("STRING",)
        # RETURN_NAMES = ("image_output_name",)

        FUNCTION = "save"

        # OUTPUT_NODE = False

        CATEGORY = "Example"

    def check_lazy_status(self, qdrant_endpoint, print_to_screen):
        """
            Return a list of input names that need to be evaluated.

            This function will be called if there are any lazy inputs which have not yet been
            evaluated. As long as you return at least one field which has not yet been evaluated
            (and more exist), this function will be called again once the value of the requested
            field is available.

            Any evaluated inputs will be passed as arguments to this function. Any unevaluated
            inputs will have the value None.
        """
        if print_to_screen == "enable":
            return ["qdrant_endpoint", "collection_name"]
        else:
            return []

    def save(self, id, title, link, vector, metadata, qdrant_endpoint, collection_name, print_to_screen):
        client = QdrantClient(qdrant_endpoint)
        collections = client.get_collections()
        if not any(collection_name == c.name for c in collections.collections):
            client.create_collection(collection_name)
        collection = client.get_collection(collection_name)
        if collection.status != CollectionStatus.Active:
            client.activate_collection(collection_name)
        client.insert(collection_name, [vector], [id], [{**metadata, "title": title, "link": link}])


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "QDrantSaver": QDrantSaver
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "QDrantSaver": "QDrant Saver Node"
}
