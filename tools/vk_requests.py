from datetime import datetime
from typing import Any, Optional
import httpx

from .. import config

class VkRequests:
    API_URL = "api.vk.com"

    @classmethod
    def __get(cls, method: str, params: dict[str, Any]) -> dict:
        try:
            response = httpx.get(
                url=f"https://{cls.API_URL}/method/{method}",
                headers={
                    "Authorization": f"Bearer {config.VK_TOKEN}"
                },
                params=params
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code}")
            raise
        except httpx.RequestError as e:
            print(f"Error during request: {str(e)}")
            raise
        
        data: dict = response.json().get('response', {})
        return data
    
    @classmethod
    def get_posts(
        cls,
        date_limit: datetime,
        domain: Optional[str] = None,
        owner_id: Optional[int] = None,
        count: int = 100,
        offset: int = 0,
    ):
        if domain is None and owner_id is None:
            raise ValueError("Either 'domain' or 'owner_id' must be provided")
        
        timestamp: int = int(date_limit.timestamp())
        method = "wall.get"
        
        params: dict = {
            "offset": offset,
            "count": count,
            "v": config.API_VERSION,
        }
        if domain is not None:
            params["domain"] = domain
        else:
            params["owner_id"] = owner_id

        response: dict = cls.__get(method, params)
        post_list: list[dict] = response.get('items', [])

        if not post_list:
            return
        
        if post_list[-1]["date"] < timestamp:
            yield list(filter(lambda x: x["date"] >= timestamp, post_list))
        else:
            while post_list[-1]["date"] >= timestamp:
                yield post_list
                if len(post_list) < count:
                    break
                offset += len(post_list)
                params["offset"] = offset
                post_list = cls.__get(method, params).get('items', [])
            else:
                yield list(filter(lambda x: x["date"] >= timestamp, post_list))


    @classmethod
    def get_comments(cls, owner_id: int, post_id: int, count: int = 100, offset: int = 0):
        """Получение комментариев для поста"""
        method = "wall.get"

        params: dict = {
            "owner_id": owner_id,
            "post_id": post_id,
            "offset": offset,
            "count": count,
            "v": config.API_VERSION,
        }
        
        response: dict = cls.__get(method, params)
        comments_count: int = response.get('count', 0)
        comments_list: list[dict] = response.get('items', [])

        if not comments_list:
            return
        
        while comments_count > 0:
            yield comments_list
            if len(comments_list) < count:
                break
            comments_count -= len(comments_list)
            params["offset"] += len(comments_list)
            comments_list = cls.__get(method, params).get('items', [])
        
        if comments_list:
            yield comments_list
        



    @classmethod
    def get_likes(cls, domain: Optional[str] = None, owner_id: Optional[int] = None) -> list[dict]:
        """Получение лайков для поста"""
        ...
