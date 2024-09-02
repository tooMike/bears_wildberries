from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import get_product_info
from app.core.db import get_async_session
from app.crud.background_tasks import save_or_update_product
from app.crud.product import product_crud
from app.schemas.schemas import (ProductResponse, SizeResponse,
                                 SizeWarehouseResponse)

# from app.api.tasks import save_product_async_task

router = APIRouter()


@router.get(
    "/{nm_id}",
    response_model=ProductResponse
)
async def get_product(
        nm_id: int,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_async_session),
) -> ProductResponse | dict:
    """Получение информации о товаре."""
    product = await product_crud.get_product_by_nm_id(
        nm_id=nm_id, session=session
    )
    if product:
        # Формируем и отдаем ответ
        response = ProductResponse(
            nm_id=product.nm_id,
            current_price=product.current_price,
            sum_quantity=product.sum_quantity,
            quantity_by_sizes=[
                SizeResponse(
                    size=size.size,
                    quantity_by_wh=[
                        SizeWarehouseResponse(
                            wh=association.warehouse.wh,
                            quantity=association.quantity
                        )
                        for association in size.warehouses_associations
                    ]
                )
                for size in product.sizes
            ]
        )
        return response

    # Если товара нет в БД, делаем запрос к wildberries и получаем данные
    product_data = await get_product_info(nm_id)

    # Преобразование данных в нужный формат
    product_dict = {
        "nm_id": product_data["id"],
        "current_price": product_data["salePriceU"] / 100,
        "sum_quantity": product_data["totalQuantity"],
        "quantity_by_sizes": [
            {
                "size": size["origName"],
                "quantity_by_wh": [
                    {"wh": stock["wh"], "quantity": stock["qty"]}
                    for stock in size["stocks"]
                ]
            }
            for size in product_data["sizes"] if size["stocks"]
        ]
    }

    # Записываем данные в БД в фоне
    background_tasks.add_task(save_or_update_product, product_data, session)

    return product_dict
