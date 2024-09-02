import os

import httpx
from dotenv import load_dotenv

load_dotenv()


async def get_product_info(nm_id: int) -> dict:
    """Получение информации о продукте по API."""

    url = f"{os.getenv('API_URL')}{nm_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise Exception("Товар не найден")
    else:
        return response.json()


def format_product_info(product_info: dict) -> str:
    nm_id = product_info["nm_id"]
    price = product_info["current_price"]
    sum_quantity = product_info["sum_quantity"]

    details = []
    for size_info in product_info["quantity_by_sizes"]:
        size = size_info["size"]
        details.append(f"*Размер: {size}*")
        for wh_info in size_info["quantity_by_wh"]:
            details.append(
                f"    Склад: {wh_info['wh']}, "
                f"Остаток: {wh_info['quantity']}"
            )

    details_str = "\n".join(details)

    return (
        f"*Информация о товаре: {nm_id}* \n\n"
        f"*Текущая цена:* {price:.2f} руб.\n"
        f"*Общий остаток:* {sum_quantity} шт.\n\n"
        f"*Детали по складам и размерам:*\n{details_str}"
    )
