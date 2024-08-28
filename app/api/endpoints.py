import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.schemas import ProductResponse, SizeResponse, SizeWarehouseResponse
from app.crud.product import product_crud
from app.crud.size import size_crud
from app.crud.size_warehouse import size_warehouse_crud


router = APIRouter()


@router.get(
    '/{nm_id}',
    response_model=ProductResponse
)
async def get_product(
        nm_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Получение информации о товаре."""
    product = await product_crud.get(obj_id=nm_id, session=session)
    if product:
        return product

    # Если товара нет в БД, делаем запрос к внешнему API
    url = f'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-2228342&spp=30&nm={nm_id}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Товар не найден")

    data = response.json()

    # Проверяем, есть ли нужные данные в ответе
    if not data.get('data', {}).get('products'):
        raise HTTPException(status_code=404, detail="Товар не найден")

    product_data = data['data']['products'][
        0]  # Предполагаем, что всегда есть хотя бы один продукт

    # Преобразование данных в нужный формат
    product_dict = {
        "nm_id": product_data['id'],
        "current_price": product_data['salePriceU'],
        "sum_quantity": product_data['totalQuantity'],
        "quantity_by_sizes": [
            {
                "size": size['origName'],
                "quantity_by_wh": [
                    {"wh": stock['wh'], "quantity": stock['qty']}
                    for stock in size['stocks']
                ]
            }
            for size in product_data['sizes'] if size['stocks']
        ]
    }

    return product_dict

