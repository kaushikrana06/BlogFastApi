from fastapi import FastAPI
from .routes import auth, blog, dashboard
from .utils.database import connect_to_mongo, close_mongo_connection


app = FastAPI()

# Event handlers for database connection
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# Including routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(blog.router, prefix="/blog", tags=["Blogs"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

