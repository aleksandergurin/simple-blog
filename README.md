To run project:
```bash
docker compose build
docker compose up
```

To create a new database schema connect to `backend` container:
```bash
docker compose exec backend bash
```

Run alembic upgrade:
```bash
flask db upgrade
```

After that you can run HTTP queries from `testing.http`
(you can use PyCharm for that or implement same queries with curl).

Short description in `docker-compose.yml` we run three services
`db`, `backend` and `proxy`. First one is Postgres DB,
second - Flask API, third - Nginx proxy.

Database credentials specified as env variables (see: `./backend/blog/config.py`).
For development environment we provide DB credentials from `./backend/env/postgres.env`.
Secret key also provided as env variable (see: `./backend/env/webapp.env`).

Shor summary of API service modules:
- `blog/models.py` contains SQLAlchemy models
- `blog/validators.py` pydantic input validators
- `blog/config.py` configuration for the application
- `blog/auth.py` API endpoints for authentication
- `blog/posts.py` API endpoints to access posts and comments

REST API authentication endpoints:
- `/auth/register` POST `username`, `email` and `password` to create a new user
- `/auth/login` POST `username` and `password` to log in
- `/auth/logout` GET to log out
- `/auth/is-authenticated` GET information about session
- `/auth/csrf` GET CSRF token

REST API posts and comments endpoints (authentication required):
- `/api/post` GET list of posts
- `/api/post` POST `title` and `content` to add a new post
- `/api/post/<int:post_id>` GET post by ID
- `/api/post/<int:post_id>/comment` GET list of comments for a post with ID
- `/api/post/<int:post_id>/comment` POST `content` to add a new comment for a post
- `/api/author/<int:author_id>/post` GET posts created by the specified author
- `/api/author/<int:author_id>/comment` GET comments created by the specified author
