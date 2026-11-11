import json
import sys
import uuid
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def post(url, key, body):   #СЃС‚РІРѕСЂ РїРѕСЃС‚ Р·Р°РїРёС‚
    request = Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Idempotency-Key": key
        }
    )

    with urlopen(request, timeout=20) as response:  #РІС–РґРїСЂР°РІР»СЏС”Рј Р·Р°РїРёС‚ РЅР° Р°РІСЃ
        return response.status, response.read()   #РєРѕРґ РІС–РґРїРѕРІС–РґС– С– С‚С–Р»Рѕ


def main():
    if len(sys.argv) != 2:
        print("Usage: python tests/check_idempotency_live.py BASE_URL")
        return 2

    url = sys.argv[1].rstrip("/") + "/api/products"   #С„РѕСЂРјСѓС”Рј Р°РґСЂРµСЃСѓ

    key = "lab7task-" + str(uuid.uuid4())  #СЃС‚РІРѕСЂ РєР»СЋС‡
    name = "Idempotency demo " + key

    body = json.dumps({
        "name": name,
        "description": "Task 7 duplicate POST test",
        "price": 100,
        "stock_quantity": 10,
        "Subcategories_id": 1
    }).encode("utf-8")

    try:   #2 СЂР°Р·Рё РЅР°РґСЃРёР»Р°С”РјРѕ РїРѕСЃС‚
        first_status, first_body = post(url, key, body)
        second_status, second_body = post(url, key, body)

    except (HTTPError, URLError) as error:
        print("HTTP/connection error:", error)
        return 1

    first = json.loads(first_body)
    second = json.loads(second_body)

    assert first_status == second_status == 201
    assert first == second
    assert first["id"] == second["id"]
    assert first_body == second_body

    print("PASS: two identical POST responses")
    print("HTTP status: 201, 201")
    print("Idempotency-Key:", key)
    print("Product ID:", first["id"])
    print("Product name:", name)

    print("Verify in MySQL that this SQL returns 1:")
    print(
        "SELECT COUNT(*) AS product_count "
        "FROM products WHERE name = '" + name + "';"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
