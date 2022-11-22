from typing import List
from typing import Optional

from fastapi import Request


class UserCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.email: Optional[str] = None
        self.password: Optional[str] = None
        self.password2: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("name")
        self.email = form.get("email")
        self.password = form.get("pwd")
        self.password2 = form.get("pwd2")

    async def is_valid(self):
        if not self.username or not len(self.username) > 2:
            self.errors.append("Username should be more than 2 characters")
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Please enter an email")
        if not self.password:
            self.errors.append("Please enter a password")
        if self.password != self.password2:
            self.errors.append("The entered passwords do not match")
        if not self.errors:
            return True
        return False
