
def create_description(data: list[str]) -> str:
    return '-&&-'.join(data)


def desc_to_list(data: str) -> list[str]:
    return data.split('-&&-')

def type_to_suffix(product_type: str):
    if product_type == 'штучный':
        return 'шт.'
    elif product_type == 'весовой':
        return 'г.'
    elif product_type == 'жидкость':
        return 'мл.'
    else:
        return ''