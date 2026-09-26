# Travel Blog API

A production-ready FastAPI backend for a travel storytelling platform. Features hierarchical locations, ordered content blocks, JWT-based authentication, and PostgreSQL integration.

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- (Optional) Python 3.11+ if running locally

### Running with Docker (Recommended)
1. Clone the repository.
2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at `http://localhost:8000`.
4. Swagger documentation: `http://localhost:8000/docs`.

### Running Locally
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Set up your `.env` file with your PostgreSQL connection string.
3. Run migrations:
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```
4. Run the seed script:
   ```bash
   python -m scripts.seed
   ```
5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🏗️ Architecture

- **Routers**: FastAPI endpoints definition using API routers.
- **Services**: Business logic layer (auth, file storage, story aggregation).
- **Repositories**: Data access layer using SQLAlchemy Async.
- **Models**: Database schema definitions with SQLAlchemy ORM.
- **Schemas**: Pydantic models for request/response validation.

## 🔑 Key Features
- **Hierarchical Locations**: Supports nested locations (e.g., City -> Region -> Country).
- **Ordered Content**: Content blocks within stories can be ordered using `ordering_index`.
- **JWT Auth**: Secure routes with JSON Web Token authentication.
- **JSONB Support**: Metadata stored as JSONB for flexible storage.
- **Image Upload**: Multi-part upload support for story contents.

## 🛠️ API Sample Request

### Create a Story
**POST** `/api/v1/stories/`
```json
{
  "name": "Summer in Bali",
  "description": "A wonderful week in paradise.",
  "author_id": 1,
  "location_id": 5,
  "content_links": [
    { "content_id": 10, "ordering_index": 0 },
    { "content_id": 12, "ordering_index": 1 }
  ]
}
```
uvicorn app.main:app --reload

admin@example.com
admin123