from openai import OpenAI
import json

api_key = 'sk-UxhWtO6rVlk4t14LzIxy9xwqEOt_uzEKkKndmupvv-T3BlbkFJB6UsmPJh03nL_Os0JfnfW3R60tiuFlTWV0qdm5CckA'
client = OpenAI(api_key=api_key)


# Функция поиска товара
def search_product(name):
    name_lower = name.lower()
    matching_products = [product for product in products if name_lower in product['name'].lower()]

    if matching_products:
        product = matching_products[0]  # Возьмем первый совпадающий товар
        return f"Товар найден: {product['name']} по цене ${product['price']}. ID продукта: {product['id']}"
    return "Товар не найден"

# Функция создания заказа
def create_order(id, item):
    for product in products:
        if product['id'] == item:
            return f"Заказ создан для клиента {id} на продукт {product['name']} по цене ${product['price']}"
    return "Ошибка: Продукт не найден"

# Определяем функции для AI
functions = [
    {
        "name": "search_product",
        "description": "Ищет товары компаний по названию",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Название продукта, например, AirPods 3"
                }
            },
            "required": ["name"],
        },
    },
    {
        "name": "create_order",
        "description": "Создает заказ для клиента",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "ID пользователя, например, 15"
                },
                "item": {
                    "type": "integer",
                    "description": "ID продукта, например, 15"
                }
            },
            "required": ["id", "item"],
        },
    }
]

messages = [
    {'role': 'system', 'content': 'Вы менеджер по продажам магазина аксессуаров BayOne. Вы работаете через ватсап и ваша задача - поговорить с клиентами, предлагать товары и ПРОДАТЬ как можно больше товаров. ID клиента: 15'}
]

def chat_with_ai(user_input):
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        functions=functions,
        function_call="auto",
    )

    response_message = response.choices[0].message

    if response_message.function_call:
        function_name = response_message.function_call.name
        function_args = json.loads(response_message.function_call.arguments)

        if function_name == "create_order":
            function_response = create_order(**function_args)
            messages.append({
                "role": "system",
                "name": function_name,
                "content": function_response,
            })

        elif function_name == "search_product":
            function_response = search_product(**function_args)

            messages.append({
                "role": "system",
                "name": function_name,
                "content": function_response,
            })

        second_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        final_response = second_response.choices[0].message.content

        print(final_response)
    else:
        print(response_message.content)

# Запуск чата
while True:
    user_input = input("Вы: ")
    if user_input.lower() in ['выход', 'exit']:
        break
    chat_with_ai(user_input)
