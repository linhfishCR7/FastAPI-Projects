from pydantic import BaseModel
from typing import List

class User(BaseModel):
    username: str
    email: str
    hashed_password: str

# In-memory "database"
fake_users_db: List[User] = []

## inserting fake data to validate the user
fake_users_db.append(User(username='admin', email='admin@admin.com', hashed_password='$2b$12$8WQHQ7AWDlmZBCwBfeFNPehYTYE0h.g.yz7qNClUaVGR5zDHAi3kK'))
blocklist_token =[]


## auth_skip_url
_auth_skip = {'auth/register', 'auth/token'}
