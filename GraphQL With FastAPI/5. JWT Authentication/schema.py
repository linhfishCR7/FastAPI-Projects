import strawberry
from typing import List, Optional
from sqlalchemy.future import select
from models import Book, User
from db import AsyncSessionLocal
from auth import create_access_token, authenticate_user, IsAuthenticated


@strawberry.type
class LoginResponse:
    access_token: str
    token_type: str = "bearer"


@strawberry.type
class BookType:
    id: int
    title: str
    author: str


@strawberry.type
class UserType:
    id: int
    username: str


@strawberry.type
class Query:

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def books(self) -> List[BookType]:
        """
            Retrieve all books.
        """
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Book))
            books = result.scalars().all()
            return [BookType(id=b.id, title=b.title, author=b.author) for b in books]

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def book(self, id: int) -> Optional[BookType]:
        """
            Retrieve a book by its ID.
        """
        async with AsyncSessionLocal() as session:
            book = await session.get(Book, id)
            if not book:
                return None
            return BookType(id=book.id, title=book.title, author=book.author)

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def greeting(self, name: Optional[str] = None) -> str:
        """
            Return a greeting message.
        """
        if name:
            return f"Hello, {name}!"
        return "Hello, stranger!"


@strawberry.type
class Mutation:

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create_book(self, title: str, author: str, info: strawberry.types.Info = None) -> BookType:
        """
            Create a new book entry.
        """
        async with AsyncSessionLocal() as session:
            new_book = Book(title=title, author=author)
            session.add(new_book)
            await session.commit()
            await session.refresh(new_book)
            return BookType(id=new_book.id, title=new_book.title, author=new_book.author)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update_book(self, id: int, title: str, author: str, info: strawberry.types.Info = None) -> Optional[BookType]:
        """
            Update a book's details.
        """
        async with AsyncSessionLocal() as session:
            book = await session.get(Book, id)
            if not book:
                return None
            book.title = title
            book.author = author
            await session.commit()
            await session.refresh(book)
            return BookType(id=book.id, title=book.title, author=book.author)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def delete_book(self, id: int, info: strawberry.types.Info = None) -> bool:
        """
            Delete a book by its ID.
        """
        async with AsyncSessionLocal() as session:
            book = await session.get(Book, id)
            if not book:
                return False
            await session.delete(book)
            await session.commit()
            return True

    @strawberry.mutation
    async def login(self, username: str, password: str) -> LoginResponse:
        """
        Simple user login to obtain JWT token.
        Params:
            username: str - user's username
            password: str - user's password
        """
        user = await authenticate_user(username, password)
        if not user:
            raise Exception("Invalid username or password")
        access_token = create_access_token(data={"sub": user.username})
        return LoginResponse(access_token=access_token)

    @strawberry.mutation
    async def register(self, username: str, password: str) -> UserType:
        """
        Simple user registration.

        Prams:
            username: str - desired username
            password: str - desired password
        """
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).filter_by(username=username))
            existing = result.scalars().first()
            if existing:
                raise Exception("Username already exists")
            user = User(username=username, password=password)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return UserType(id=user.id, username=user.username)


schema = strawberry.Schema(Query, Mutation)
