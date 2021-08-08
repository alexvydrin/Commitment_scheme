"""
Commitment scheme
способ фиксации утверждения без раскрытия самого утверждения или раскрытия его позже

Общая задача:
требуется реализовать схему с использованием преобразований в группе точек эллиптической кривой
выберем SECP256k1 - the Bitcoin elliptic curve
private key = 32 байта (256 бит)
public key uncompressed = 65 байт  = 1 байт (04) + 32 байта + 32 байта
signature = 64 байта

Постановка задачи:
Алиса говорит Бобу что точно знает какая команда выиграет чемпионат, но пока не может сказать
Боб требует доказательств, справедливо полагая что Алиса может изменить решение после чемпионата
Тогда Алиса присылает Бобу два числа:
1) signature - подпись сообщения
2) vk - публичный ключ для проверки подписи
После чемпионата можно будет доказать что была выбрана именно эта команда прислав message
и проверить что подпись правильная
*) для усложнения задачи можно использовать соль - дополнительные случайные слова для шифрования
"""

# noinspection PyProtectedMember
from ecdsa import SigningKey, SECP256k1, BadSignatureError

# Сообщение - его будем подписывать
message = b"Manchester United is a new champion"
print('message=', message)
print('message_hex=', message.hex())

# Получаем private key
# Каждый раз он создается новый
sk = SigningKey.generate(curve=SECP256k1)
print('vk = ', sk.to_pem())
vk_hex = sk.to_string().hex()
print('vk_hex=', vk_hex)

# Получаем public key на основании private key
# vk = sk.verifying_key
# или
vk = sk.get_verifying_key()
print(vk.to_pem())
vk_uncompressed = vk.to_string("uncompressed").hex()
print('vk_uncompressed=', vk_uncompressed)
vk_compressed = "{0}".format(vk.to_string("compressed").hex())
print('vk_compressed=', vk_compressed)

# Получаем подпись для сообщения
signature = sk.sign(message)
print('signature=', signature)
print('signature_hex=', signature.hex())

# Бобу передается только signature и vk
# После окончания чемпионата для проверки передается message
# Боб проверяет не было ли изменено сообщение

try:
    vk.verify(signature, b"Manchester United is a new champion")
    print("good signature")
except BadSignatureError:
    print("BAD SIGNATURE")

try:
    vk.verify(signature, b"Liverpool City Football Club is a new champion")
    print("good signature")
except BadSignatureError:
    print("BAD SIGNATURE")
