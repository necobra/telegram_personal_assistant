import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    users_list = [int(userid) for userid in os.getenv("USER_LIST").split(",")]  # admins and notification
    groups_list = [-4188484276]


config = Config()
