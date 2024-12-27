from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry

# Create the registry
mapper_registry = registry()

# Create the base class for declarative models
Base = declarative_base()