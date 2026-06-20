#(©)Codexbotz
#rymme

import time
import html
from aiohttp import web

from config import BASE_URL, VERIFY_TOKEN_TTL, VERIFY_MIN_SECONDS, VERIFY_EXPIRE
from helper_func import decrypt_payload, get_shortlink, gen_cookie
from database.database import (
    get_verify_token,
    set_verify_redirecting,
    set_verify_used,
    update_verify_status,
)

routes = web.RouteTableDef()


def _fail_page(reason: str, bot: str = None, status: int = 403) -> web.Response:
    back = f'<a href="https://t.me/{html.escape(bot)}" style="display:inline-block;margin-top:18px;padding:12px 22px;background:#0088cc;color:#fff;border-radius:8px;text-decoration:none;">↩ Back to Bot</a>' if bot else ""
    body = f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Verification Failed</title></head>
<body style="font-family:system-ui,Arial,sans-serif;background:#0e1621;color:#e6edf3;text-align:center;padding:48px 20px;">
<div style="max-width:440px;margin:0 auto;background:#17212b;padding:32px;border-radius:14px;">
<div style="font-size:42px;">⛔</div>
<h2>Verification Failed</h2>
<p style="color:#9fb0c0;">{html.escape(reason)}</p>
<p style="color:#9fb0c0;">Please open the link again <b>from the bot</b> and complete it without skipping. Bypassing is not allowed.</p>
{back}
</div></body></html>"""
    return web.Response(text=body, content_type="text/html", status=status)


@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("CodeXBotz")


@routes.get("/link/{uid}/{token}")
async def verify_link_handler(request):
    uid = request.match_info["uid"]
    blob = request.match_info["token"]

    data = decrypt_payload(blob, ttl=VERIFY_TOKEN_TTL)
    if not data or str(data.get("uid")) != str(uid):
        return _fail_page("This link is invalid or has expired.")

    doc = await get_verify_token(data.get("tid"))
    if not doc:
        return _fail_page("This link is invalid or has expired.", bot=data.get("bot"))
    if doc.get("state") != "issued":
        return _fail_page("This link was already used. Request a fresh one from the bot.", bot=data.get("bot"))

    cookie = gen_cookie()
    await set_verify_redirecting(data["tid"], cookie, time.time())

    confirm_url = f"{BASE_URL}/confirm/{uid}/{blob}"
    short = await get_shortlink(confirm_url)

    resp = web.HTTPFound(short)
    resp.set_cookie("vrf", cookie, max_age=VERIFY_TOKEN_TTL, httponly=True, samesite="Lax")
    return resp


@routes.get("/confirm/{uid}/{token}")
async def verify_confirm_handler(request):
    uid = request.match_info["uid"]
    blob = request.match_info["token"]

    data = decrypt_payload(blob, ttl=VERIFY_TOKEN_TTL)
    if not data or str(data.get("uid")) != str(uid):
        return _fail_page("This link is invalid or has expired.")

    bot = data.get("bot")
    doc = await get_verify_token(data.get("tid"))
    if not doc:
        return _fail_page("This link is invalid or has expired.", bot=bot)
    if doc.get("state") != "redirecting":
        return _fail_page("Open the verification link from the bot first — don't skip steps.", bot=bot)

    cookie = request.cookies.get("vrf")
    if not cookie or cookie != doc.get("cookie"):
        return _fail_page("Verification must be completed in the same browser. Bypass detected.", bot=bot)

    link_at = doc.get("link_at") or 0
    if time.time() - link_at < VERIFY_MIN_SECONDS:
        return _fail_page("You completed this too fast — please solve the link properly.", bot=bot)

    await set_verify_used(data["tid"])
    await update_verify_status(int(uid), time.time() + VERIFY_EXPIRE)

    return web.HTTPFound(f"https://t.me/{bot}?start={data.get('fp')}")
