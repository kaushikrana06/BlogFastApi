# BlogFastAPI

## Overview
This document provides an overview of the endpoints available in the BlogFastAPI. The API is built using FastAPI and hosted at [https://blogfastapi.onrender.com](https://blogfastapi.onrender.com). It offers features for user authentication, blog creation, and a dashboard for personalized content.

## Endpoints

### Authentication (`auth` router)
- **Register User**
  - **Method:** POST
  - **URL:** `https://blogfastapi.onrender.com/auth/register`
  - **Description:** Registers a new user.
  - **JSON Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "yourpassword"
    }
    ```

- **Login**
  - **Method:** POST
  - **URL:** `https://blogfastapi.onrender.com/auth/login`
  - **Description:** Logs in a user and returns an access token.
  - **JSON Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "yourpassword"
    }
    ```

- **Update User**
  - **Method:** PUT
  - **URL:** `https://blogfastapi.onrender.com/auth/users/{user_id}`
  - **Description:** Updates user information.
  - **JSON Body:**
    ```json
    {
      "email": "newemail@example.com",
      "password": "newpassword"
    }
    ```

- **Add Tags to User**
  - **Method:** POST
  - **URL:** `https://blogfastapi.onrender.com/auth/users/{user_id}/tags`
  - **Description:** Adds tags to a user.
  - **JSON Body:**
    ```json
    {
      "tags": [
        {"name": "tag1", "like": 1},
        {"name": "tag2", "like": 0}
      ]
    }
    ```

- **Remove Tags from User**
  - **Method:** DELETE
  - **URL:** `https://blogfastapi.onrender.com/auth/users/{user_id}/tags`
  - **Description:** Removes tags from a user.
  - **JSON Body:**
    ```json
    {
  "tags": ["tag1", "tag2"]
  }

    ```

### Blogs (`blog` router)
- **Create Blog**
  - **Method:** POST
  - **URL:** `https://blogfastapi.onrender.com/blog/`
  - **Description:** Creates a new blog entry.
  - **JSON Body:**
    ```json
    {
      "title": "Blog Title",
      "content": "Blog content...",
      "owner_id": "user_id",
      "tags": ["tag1", "tag2"]
    }
    ```

- **Get Blogs (with Pagination)**
  - **Method:** GET
  - **URL:** `https://blogfastapi.onrender.com/blog/?skip=0&limit=10`
  - **Description:** Retrieves a paginated list of blogs.

- **Get Specific Blog**
  - **Method:** GET
  - **URL:** `https://blogfastapi.onrender.com/blog/{blog_id}`
  - **Description:** Retrieves a specific blog by ID.

- **Update Blog**
  - **Method:** PUT
  - **URL:** `https://blogfastapi.onrender.com/blog/{blog_id}`
  - **Description:** Updates a specific blog.
  - **JSON Body:**
    ```json
    {
      "title": "Updated Title",
      "content": "Updated content..."
    }
    ```

- **Delete Blog**
  - **Method:** DELETE
  - **URL:** `https://blogfastapi.onrender.com/blog/{blog_id}`
  - **Description:** Deletes a specific blog.

### Dashboard (`dashboard` router)
- **Get User Blogs (with Pagination)**
  - **Method:** GET
  - **URL:** `https://blogfastapi.onrender.com/dashboard/user/{user_id}/blogs?skip=0&limit=10`
  - **Description:** Retrieves blogs based on a user's preferences in a paginated format.

## Usage Notes
- Replace `{user_id}` and `{blog_id}` with the actual user ID or blog ID in the request.
- Ensure that the correct HTTP method (GET, POST, PUT, DELETE) is used for each URL.
- Some URLs may require authentication (access token) or specific parameters/body.
- Adjust `skip` and `limit` for pagination as needed.

