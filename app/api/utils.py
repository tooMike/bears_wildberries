import httpx
from fastapi import HTTPException


async def get_product_info(nm_id):
    """Получение инфморации о товаре с Wildberries."""
    url = (f'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest'
           f'=-2228342&spp=30&nm={nm_id}')
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Товар не найден")

    data = response.json()

    # Проверяем, есть ли нужные данные в ответе
    if not data.get('data', {}).get('products'):
        raise HTTPException(status_code=404, detail="Товар не найден")

    # Предполагаем, что всегда есть хотя бы один продукт
    product_data = data['data']['products'][0]

    return product_data
