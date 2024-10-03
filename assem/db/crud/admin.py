from sqlalchemy.orm import Session

from assem.db.models import Business, Product


def get_products(
    platform: str,
    db: Session,
    search: str = None,
    skip: int = 0,
    limit: int = 15,

):
    # Найти бизнесы по platform
    businesses = db.query(Business).filter(Business.platformid == platform).all()
    if not businesses:
        raise ValueError("Бизнесы не найдены по указанной платформе")

    # Получить список ID бизнесов
    business_ids = [business.id for business in businesses]

    # Формируем базовый запрос для поиска продуктов
    query = db.query(Product).filter(Product.business_id.in_(business_ids))

    # Если параметр поиска не пустой, добавляем фильтрацию по ключевым словам
    if search:
        query = query.filter(Product.keyword.ilike(f'%{search}%'))  # Ищем по ключевым словам

    # Получаем продукты с пагинацией
    products = query.offset(skip).limit(limit).all()

    return [product_to_dict(product) for product in products]

def product_to_dict(product):
    return {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "keyword": product.keyword,
        # Добавьте другие поля, которые хотите вернуть
    }
