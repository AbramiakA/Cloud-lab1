import { Counter, Rate } from "k6/metrics";
import http from "k6/http";
import { check, sleep } from "k6";

const BASE_URL = (__ENV.BASE_URL || "http://localhost:5000").replace(/\/$/, "");
const TARGET_VUS = Number(__ENV.TARGET_VUS || 80);
const cacheHits = new Counter("cache_hits");
const cacheMisses = new Counter("cache_misses");
const cacheHitRatio = new Rate("cache_hit_ratio");

export const options = {
    stages: [
        { duration: "3m", target: TARGET_VUS },
        { duration: "5m", target: TARGET_VUS },
        { duration: "2m", target: 0 }
    ],
    summaryTrendStats: [
        "avg",
        "min",
        "max",
        "p(50)",
        "p(95)",
        "p(99)"
    ]
};

function parseJson(response) {
    try {
        return response.json();
    } catch (error) {
        return null;
    }
}

export default function () {
    //створ новий товар
    const product = {
        name: `Load test ${__VU}-${__ITER}-${Date.now()}`,
        description: "Created during k6 load testing",
        price: 100,
        stock_quantity: 10,
        Subcategories_id: 1
    };

    const postResponse = http.post(
        `${BASE_URL}/api/products`,
        JSON.stringify(product),
        {
            headers: {
                "Content-Type": "application/json"
            },
            tags: {
                name: "POST /api/products"
            }
        }
    );

    check(postResponse, {
        "Product created (201)": (r) => r.status === 201
    });

    const createdProduct = parseJson(postResponse);
    const createdId = createdProduct && Number.isInteger(createdProduct.id)
        ? createdProduct.id
        : null;

    //читаємо одну сторінку каталогу(по 20 товарів)
    const catalogResponse = http.get(
        `${BASE_URL}/api/products?page=1&limit=20`,  //пагінація
        {
            tags: {
                name: "GET /api/products?page=1&limit=20"
            }
        }
    );

    const catalog = parseJson(catalogResponse);

    check(catalogResponse, {
        "Catalog page read (200)": (r) =>
            r.status === 200 && Array.isArray(catalog)
    });

    const catalogIds = Array.isArray(catalog)
        ? catalog
            .filter((item) => item && Number.isInteger(item.id))
            .map((item) => item.id)
            .filter((id) => id !== createdId)
        : [];

    //берем 8 товарів (перший щойно створений)
    const fallbackId = createdId || catalogIds[0] || 1;
    const productIds = [fallbackId];

    //ще 7
    for (let i = 0; i < 7; i++) {
        const id = catalogIds.length > 0
            ? catalogIds[(i + __VU + __ITER) % catalogIds.length]
            : fallbackId;

        productIds.push(id);
    }

    //8 гет запитів до окремих товарів
    for (let i = 0; i < productIds.length; i++) {
        const productId = productIds[i];

        const getResponse = http.get(
            `${BASE_URL}/api/products/${productId}`,
            {
                tags: {
                    name: "GET /api/products/:id"
                }
            }
        );

        const cacheStatus = String(
            getResponse.headers["X-Cache"] || ""
        ).toUpperCase();

        if (cacheStatus === "HIT") {
            cacheHits.add(1);
            cacheHitRatio.add(true);
        } else if (cacheStatus === "MISS") {
            cacheMisses.add(1);
            cacheHitRatio.add(false);
        }

        check(getResponse, {
            "Product read (200)": (r) => r.status === 200
        });

        if (i === 0 && createdId !== null) {
            const receivedProduct = parseJson(getResponse);

            check(getResponse, {
                "Correct product ID": () =>
                    receivedProduct !== null &&
                    receivedProduct.id === createdId
            });
        }
    }

    sleep(1);
}
