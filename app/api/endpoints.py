import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.warehouse import warehouse_crud
from app.models import Product, Size, SizeWarehouseAssociation, Warehouse
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
    product = await product_crud.get_product_by_nm_id(
        nm_id=nm_id, session=session
    )
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

    # Предполагаем, что всегда есть хотя бы один продукт
    product_data = data['data']['products'][0]

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

    product = Product(
        nm_id=product_data['id'],
        current_price=product_data['salePriceU'],
        sum_quantity=product_data['totalQuantity'],
    )

    # Создание и добавление размеров и складов
    with session.no_autoflush:
        for size_data in product_data['sizes']:
            if size_data['stocks']:
                size = Size(
                    size=size_data['origName'],
                    product=product  # Устанавливаем связь с продуктом
                )
                size_warehouse = 0

                # Добавляем записи в промежуточную таблицу SizeWarehouseAssociation
                for stock in size_data['stocks']:
                    warehouse = await warehouse_crud.get_warehouse_by_wh(
                        wh=stock['wh'], session=session
                    )
                    if not warehouse:
                        # Если склада нет, создаем новый
                        warehouse = Warehouse(wh=stock['wh'])
                        session.add(warehouse)
                        # Сохраняем промежуточно, чтобы получить ID склада
                        await session.flush()
                    size_warehouse_association = SizeWarehouseAssociation(
                        id=size_warehouse+1,
                        size=size,
                        warehouse=warehouse,
                        quantity=stock['qty']
                    )
                    session.add(size_warehouse_association)

                session.add(size)

    # Сохраняем продукт и связанные данные (размеры и склады) в базу данных
    session.add(product)
    await session.commit()
    await session.refresh(product)

    return product_dict

