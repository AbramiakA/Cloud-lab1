import hashlib
import json
import os
import re
import secrets

from redis import Redis, RedisError


RESULT_TTL = 24 * 60 * 60  #24 год
PROCESSING_TTL = 5 * 60    #5 хв для незавершеного запиту

_redis = None


class IdempotencyError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code


def _client():
    global _redis #створ редіс клієнта

    if _redis is None:
        url = os.getenv("REDIS_URL")

        if not url:
            raise RedisError("REDIS_URL is not configured")

        _redis = Redis.from_url(
            url,
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1
        )

    return _redis


#якщо ключ належить запиту можна завершити
#шоб безпечно зберегти операцію в редіс і не перезаписати ключ іншого запиту
_COMPLETE = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    return redis.call('SET', KEYS[1], ARGV[2], 'EX', ARGV[3])
end
return nil
"""

#якщо помилка створення то видаляєм свій ключ
_RELEASE = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    return redis.call('DEL', KEYS[1])
end
return 0
"""


def create_once(idempotency_key, data, create_product): #створ 1 товар для 1 клююча
    #перевірка чи валідний ключ
    if not re.fullmatch(r"[A-Za-z0-9._:-]{1,128}", idempotency_key):
        raise IdempotencyError("Invalid Idempotency-Key", 400)

    body = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    )

    #шоб перевірити чи різні дані товарів
    fingerprint = hashlib.sha256(
        body.encode("utf-8") #перетворює текст на байти
    ).hexdigest()

    key_hash = hashlib.sha256(   #хешує ключ
        idempotency_key.encode("utf-8")
    ).hexdigest()

    redis_key = f"idempotency:products:create:{key_hash}"  #формуєм цей ключ

    pending = json.dumps({   #інфра про викоанння завдання
        "state": "processing",
        "fingerprint": fingerprint,
        "token": secrets.token_hex(16)  #кожна спроба має мати власний токен, бо клюм може бути однаковий
    }, separators=(",", ":"))

    try:
        client = _client()

        acquired = client.set(
            redis_key,
            pending,
            nx=True,   #запис якщо ключ ще не існує
            ex=PROCESSING_TTL #5хв
        )

        if not acquired:
            saved = client.get(redis_key)

            if saved is None:
                raise IdempotencyError("Retry the request", 409)

            previous = json.loads(saved)

            if previous["fingerprint"] != fingerprint:
                raise IdempotencyError(
                    "Key reused with different data", 409
                )

            if previous["state"] == "processing":
                raise IdempotencyError(
                    "Request already in progress", 409
                )

            return previous["body"], previous["status"]

    except (RedisError, ValueError, KeyError) as exc:
        raise IdempotencyError(
            "Idempotency storage unavailable", 503
        ) from exc

    try:
        product = create_product(data) #якщо ключа нема створ дані

    except Exception:
        try:
            client.eval(_RELEASE, 1, redis_key, pending) #видалям ключ
        except RedisError:
            pass
        raise

    finished = json.dumps({  #тут те шо ми хочемо зберігати 24год
        "state": "done",
        "fingerprint": fingerprint,
        "status": 201,
        "body": product
    }, ensure_ascii=False, separators=(",", ":"))

    try:
        stored = client.eval(
            _COMPLETE,
            1,
            redis_key,
            pending,
            finished,
            RESULT_TTL
        )

    except RedisError as exc:
        raise IdempotencyError(
            "Could not save idempotent result", 503
        ) from exc

    if not stored:
        raise IdempotencyError(
            "Idempotency reservation expired", 503
        )

    return product, 201
