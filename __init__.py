from .comfyui_qdrant_saver import QDrantSaver

NODE_CLASS_MAPPINGS = {
    "QDrantSaver": QDrantSaver
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "QDrantSaver": "QDrant Saver Node"
}
