# Python Chatter
Python Chatter is a RESTful API backend for a blogging platform, built with Python. It provides endpoints for publishing articles, user authentication, commenting, and user interactions.

## Features
- User registration and authentication (JWT)
- Publish, edit, and delete articles
- Comment on articles
- Like and bookmark articles
- Retrieve articles by author or topic
- Send and receive private messages between users
- RESTful API endpoints with FastAPI
- SQLite database integration
- Input validation and error handling
- API documentation with Swagger UI
- Modular and extensible codebase

## Prerequisites

- Python 3.8+
- pip
- virtualenv

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication

## Development

Start the development server with:
```bash
uvicorn app.main:app --reload
```



## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/python-chatter.git
    ```
2. Navigate to the project directory:
    ```bash
    cd python-chatter
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Create a `.env` file in the project root and add your environment variables  (e.g., secret keys, database URL).  
    You can use the provided `.env.sample` file as a template:(e.g., secret keys, database URL):
        ```env
        SECRET_KEY=your_secret_key
        DATABASE_URL=sqlite:///./python_chatter.db
        ```


## Usage

Start the API server:
```bash
python app.main:app.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
