# Author: Oleg Mrynskyi

import os
import sys
import yaml

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

def generate_openapi_yaml(output_path: str = "openapi.yaml") -> None:
    """
    Generates and writes openapi.yaml from FastAPI schema.
    """
    openapi_schema = app.openapi()
    openapi_schema["openapi"] = "3.1.0"

    # Add security schemes for Bearer Auth
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "PAT",
            "description": "GitHub Fine-Grained PAT or App Installation Token"
        }
    }

    # Attach global or route security
    openapi_schema["security"] = [{"bearerAuth": []}]

    # Ensure root path output
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    full_output_path = os.path.join(root_dir, output_path)

    with open(full_output_path, "w", encoding="utf-8") as f:
        yaml.dump(openapi_schema, f, sort_keys=False, allow_unicode=True)

    print(f"Successfully generated OpenAPI 3.1 contract at {full_output_path}")

if __name__ == "__main__":
    generate_openapi_yaml()
