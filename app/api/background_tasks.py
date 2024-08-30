from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.warehouse import warehouse_crud
from app.models import Product, Size, SizeWarehouseAssociation, Warehouse


async def save_or_update_product(product_data: dict, session: AsyncSession):
    """Сохранение или обновление информации о продукте в БД"""

    # Попробуем найти существующий продукт по nm_id
    existing_product = await session.execute(
        select(Product).where(Product.nm_id == product_data["id"])
    )
    existing_product = existing_product.scalars().first()

    if existing_product:
        existing_product.current_price = product_data["salePriceU"] / 100
        existing_product.sum_quantity = product_data["totalQuantity"]

        # Удаляем существующие связи между продуктом, размерами и складами
        await session.execute(
            delete(SizeWarehouseAssociation).where(
                SizeWarehouseAssociation.size_id.in_(
                    select(Size.id).where(
                        Size.product_id == existing_product.id
                        )
                )
            )
        )
        await session.execute(
            delete(Size).where(Size.product_id == existing_product.id)
        )

        product = existing_product

    else:
        product = Product(
            nm_id=product_data["id"],
            current_price=product_data["salePriceU"] / 100,
            sum_quantity=product_data["totalQuantity"],
        )

    # Создание и добавление размеров и складов
    for size_data in product_data["sizes"]:
        if size_data["stocks"]:
            size = Size(
                size=size_data["origName"],
                product=product
            )
            session.add(size)

            # Добавляем записи в промежуточную таблицу
            # SizeWarehouseAssociation
            for stock in size_data["stocks"]:
                warehouse = await warehouse_crud.get_warehouse_by_wh(
                    wh=stock["wh"], session=session
                )
                if not warehouse:
                    # Если склада нет, создаем новый
                    warehouse = Warehouse(wh=stock["wh"])
                    session.add(warehouse)
                    # Сохраняем промежуточно, чтобы получить ID склада
                    await session.flush()
                size_warehouse_association = SizeWarehouseAssociation(
                    size=size,
                    warehouse=warehouse,
                    quantity=stock["qty"]
                )
                session.add(size_warehouse_association)

    # Сохраняем продукт и связанные данные (размеры и склады) в базу данных
    session.add(product)
    await session.commit()
    await session.refresh(product)
