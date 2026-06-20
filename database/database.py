#(©)CodeXBotz

import pymongo, os
from config import DB_URI, DB_NAME

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']
verify_data = database['verify']

async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return


#==================== Verification gate helpers ====================#

async def update_verify_status(user_id: int, verified_until: float):
    # Mark the user verified until `verified_until` (epoch seconds).
    user_data.update_one(
        {'_id': user_id},
        {'$set': {'verified_until': verified_until}},
        upsert=True
    )
    return

async def get_verify_status(user_id: int) -> float:
    # Epoch seconds until which the user is verified (0 if never / unknown).
    found = user_data.find_one({'_id': user_id})
    if not found:
        return 0
    return found.get('verified_until', 0)

async def create_verify_token(tid: str, user_id: int, fp: str, bot: str, ts: float):
    verify_data.insert_one({
        '_id': tid,
        'uid': user_id,
        'fp': fp,
        'bot': bot,
        'state': 'issued',
        'cookie': None,
        'link_at': None,
        'created_at': ts,
    })
    return

async def get_verify_token(tid: str):
    return verify_data.find_one({'_id': tid})

async def set_verify_redirecting(tid: str, cookie: str, link_at: float):
    verify_data.update_one(
        {'_id': tid},
        {'$set': {'state': 'redirecting', 'cookie': cookie, 'link_at': link_at}}
    )
    return

async def set_verify_used(tid: str):
    verify_data.update_one(
        {'_id': tid},
        {'$set': {'state': 'used'}}
    )
    return

async def reset_verify_status(user_id: int):
    # Clear a user's verification so they must verify again on the next file.
    user_data.update_one(
        {'_id': user_id},
        {'$set': {'verified_until': 0}},
        upsert=True
    )
    return

async def count_verified(now: float) -> int:
    # Number of users currently within their verification window.
    return user_data.count_documents({'verified_until': {'$gt': now}})
