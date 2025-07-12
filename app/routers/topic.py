from fastapi import APIRouter

router = APIRouter(
    prefix="/topics",
    tags=["topics"]
)

# get all topics
# get topic by id
# create topic
# follow topic
# unfollow topic