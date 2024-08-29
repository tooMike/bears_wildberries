import asyncio

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.celery import celery_app
from app.core.db import AsyncSessionLocal, get_async_session
from app.crud.warehouse import warehouse_crud
from app.models import Product, Size, SizeWarehouseAssociation, Warehouse


SQLALCHEMY_DATABASE_URL = "sqlite:///./fastapi.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@celery_app.task
def save_product_task(product_data):
    """Сохранение информации о товаре в БД (с синхронной реализацией)."""

    # Создание новой сессии для задачи
    session = SessionLocal()

    try:
        product = Product(
            nm_id=product_data['id'],
            current_price=product_data['salePriceU'] / 100,
            sum_quantity=product_data['totalQuantity'],
        )

        for size_data in product_data['sizes']:
            if size_data['stocks']:
                size = Size(
                    size=size_data['origName'],
                    product=product
                )
                session.add(size)

                for stock in size_data['stocks']:
                    warehouse = session.execute(
                        select(Warehouse).where(
                            Warehouse.wh == stock['wh']
                        )
                    ).scalars().first()
                    if not warehouse:
                        warehouse = Warehouse(wh=stock['wh'])
                        session.add(warehouse)

                    size_warehouse_association = SizeWarehouseAssociation(
                        size=size,
                        warehouse=warehouse,
                        quantity=stock['qty']
                    )
                    session.add(size_warehouse_association)

        session.add(product)
        session.commit()
        session.refresh(product)
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


@celery_app.task
def save_product_async_task(product_data_):
    """Сохранение информации о товаре в БД (с асинхронной реализацией)."""

    async def inner(product_data):
        async with AsyncSessionLocal() as session:
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

    loop = asyncio.new_event_loop()
    loop.run_until_complete(inner(product_data_))
