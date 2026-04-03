import requests

def check_usdt(tx):
    # مثال: يمكن ربط API حقيقي لاحقًا
    if tx.startswith("T"):
        return True, 1.0  # 1 USDT
    return False, 0