from app.crud.warehouse import warehouse_crud
from app.models import Product, Size, SizeWarehouseAssociation, Warehouse


async def save_product(product_data, session):
    """Сохранение информации о продукте в БД"""

    product = Product(
        nm_id=product_data['id'],
        current_price=product_data['salePriceU'] / 100,
        sum_quantity=product_data['totalQuantity'],
    )

    # Создание и добавление размеров и складов
    for size_data in product_data['sizes']:
        if size_data['stocks']:
            size = Size(
                size=size_data['origName'],
                product=product  # Устанавливаем связь с продуктом
            )
            session.add(size)

            # Добавляем записи в промежуточную таблицу
            # SizeWarehouseAssociation
            for stock in size_data['stocks']:
                warehouse = await warehouse_crud.get_warehouse_by_wh(
                    wh=stock['wh'], session=session
                )
                if not warehouse:
                    # Если склада нет, создаем новый
                    warehouse = Warehouse(wh=stock['wh'])
                    session.add(warehouse)
                    # Сохраняем промежуточно, чтобы получить ID склада
                    # await session.flush()
                size_warehouse_association = SizeWarehouseAssociation(
                    size=size,
                    warehouse=warehouse,
                    quantity=stock['qty']
                )
                session.add(size_warehouse_association)

    # Сохраняем продукт и связанные данные (размеры и склады) в базу данных
    session.add(product)
    await session.commit()
    await session.refresh(product)
