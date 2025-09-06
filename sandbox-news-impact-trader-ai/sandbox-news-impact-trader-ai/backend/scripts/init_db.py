from backend.db import Base, engine
import backend.models
Base.metadata.create_all(engine)
print('Database tables created.')
