import importlib
import inspect
from pathlib import Path
from fastapi import APIRouter

api_router = APIRouter()

# Get the directory of the current file
router_dir = Path(__file__).parent

# Loop through all Python files in the directory
for file in router_dir.glob("*.py"):
    if file.stem != "__init__":
        # Import the module dynamically
        module_name = f"{__package__}.{file.stem}"
        module = importlib.import_module(module_name)
        # # Check if the module has a 'router' attribute and include it
        # if hasattr(module, "router"):
        #     api_router.include_router(module.router)
        # Loop through all attributes in the module
        for name, obj in inspect.getmembers(module):
            # Check if the attribute is an instance of APIRouter
            if isinstance(obj, APIRouter):
                api_router.include_router(obj)