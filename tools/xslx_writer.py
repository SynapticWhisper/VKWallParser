from datetime import datetime
from typing import Optional, List, Dict
import pandas as pd
from .vk_requests import VkRequests


def filter_post_data(posts: List[Dict]) -> List[Dict]:
    filtered_posts = []
    for post in posts:
        filtered_posts.append({
            'post_id': post['id'],
            'text': post.get('text', ''),
            'date': datetime.fromtimestamp(post['date']),
            'likes': post['likes']['count'],
            'comments': post['comments']['count']
        })
    return filtered_posts

def filter_comment_data(comments: List[Dict], post_id: int) -> List[Dict]:
    filtered_comments = []
    for comment in comments:
        filtered_comments.append({
            'post_id': post_id,
            'user_id': comment['from_id'],
            'text': comment.get('text', ''),
            'date': datetime.fromtimestamp(comment['date'])
        })
    return filtered_comments

def filter_like_data(likes: List[int], post_id: int) -> List[Dict]:
    return [{'post_id': post_id, 'user_id': user_id} for user_id in likes]

def save_to_excel(
        output_file: str,
        date_limit: datetime,
        domain: Optional[str] = None,
        owner_id: Optional[int] = None,
    ):
    """Сохранение данных в Excel файл по частям"""
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        posts_df = pd.DataFrame()
        comments_df = pd.DataFrame()
        likes_df = pd.DataFrame()

        for posts_chunk in VkRequests.get_posts(date_limit, domain, owner_id):
            filtered_posts = filter_post_data(posts_chunk)
            posts_df = pd.DataFrame(filtered_posts)
            posts_df.to_excel(writer, sheet_name='Посты', index=False, header=not writer.sheets)

            for post in posts_chunk:
                for comments_chunk in VkRequests.get_comments(post["from_id"], post["id"]):
                    filtered_comments = filter_comment_data(comments_chunk, post["id"])
                    comments_df = pd.DataFrame(filtered_comments)
                    comments_df.to_excel(writer, sheet_name='Комментарии', index=False, header=not writer.sheets)

                for likes_chunk in VkRequests.get_likes(post["from_id"], post["id"]):
                    filtered_likes = filter_like_data(likes_chunk, post["id"])
                    likes_df = pd.DataFrame(filtered_likes)
                    likes_df.to_excel(writer, sheet_name='Лайки', index=False, header=not writer.sheets)
