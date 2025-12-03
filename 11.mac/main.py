import binascii
import secrets
import time

import hmac_algo

SHARED_KEY = hmac_algo.SECRET_KEY

# Имитация базы данных использованных Nonce на стороне Получателя (Б)
USED_NONCES_B = set()


# создает пакет данных для передачи, включая MAC и NONCE
def sender_create_packet(key: bytes, message: str) -> tuple[bytes, bytes, bytes]:
    message_bytes = message.encode('utf-8')
    # генерируем уникальный NONCE (16 случайных байт)
    nonce = secrets.token_bytes(16)
    # формируем полные данные для MAC (Сообщение || Nonce)
    data_to_mac = message_bytes + nonce
    mac_tag = hmac_algo.hmac_sha256(key, data_to_mac)
    print(f"[A]: generated Nonce: {
          binascii.hexlify(nonce).decode()[:8]}...")
    return message_bytes, nonce, mac_tag


# имитирует передачу пакета по незащищенному каналу
# тупо unpack, имитируем прозрачную передачу
def transmit_packet(packet: tuple) -> tuple:
    msg, nonce, tag = packet
    return msg, nonce, tag


# проверяет Nonce и верифицирует MAC
def receiver_process_packet(key: bytes, received_packet: tuple) -> bool:
    message_bytes, nonce, received_tag = received_packet

    print(f"[B]: Packet received. Nonce: {
          binascii.hexlify(nonce).decode()[:8]}...")

    if nonce in USED_NONCES_B:
        print("FAILED: Replay Attack. Nonce has already been used")
        return False

    # create verification data (Message || Nonce)
    data_to_verify = message_bytes + nonce

    is_valid = hmac_algo.verify_mac_manual(key, data_to_verify, received_tag)

    if is_valid:
        USED_NONCES_B.add(nonce)
        print("---SUCCESS: message is authentic---")
        return True
    else:
        print("FAILURE: MAC doesn't match")
        return False


def fair():
    message_1 = "Command. Some usefull command"
    packet_1 = sender_create_packet(SHARED_KEY, message_1)
    received_1 = transmit_packet(packet_1)
    result_1 = receiver_process_packet(SHARED_KEY, received_1)
    print(f"result is: {'OK' if result_1 else 'FAILURE'}")


def mim():
    # A generates right packet and mac-tag
    message_2_orig = "Command. Retrieve all data"
    packet_2_orig = sender_create_packet(SHARED_KEY, message_2_orig)

    # Злоумышленник (М) перехватывает пакет 2
    msg_orig, nonce_orig, tag_orig = packet_2_orig

    # Злоумышленник изменяет сообщение
    msg_attack = "Command: Delete all data".encode('utf-8')
    # Злоумышленник не знает ключа, поэтому отправляет СТАРЫЙ MAC
    packet_2_attack = (msg_attack, nonce_orig, tag_orig)

    print(f"[M]: Message changed to : '{msg_attack.decode()}'")
    received_2_attack = transmit_packet(packet_2_attack)
    result_2 = receiver_process_packet(SHARED_KEY, received_2_attack)
    # HMAC не сойдется, при расчете просто будет другой Tcalc
    print(f"result is : {'SUCCESS' if result_2 else 'FAILURE'}")


def reply():
    # Отправитель А снова генерирует пакет 3
    message_3 = "Запрос на баланс."
    packet_3 = sender_create_packet(SHARED_KEY, message_3)
    received_3 = transmit_packet(packet_3)
    result_3_ok = receiver_process_packet(SHARED_KEY, received_3)
    print(f"Result is: {'OK' if result_3_ok else 'FAILURE'}")

    # Злоумышленник (М) перехватывает и сохраняет пакет 3
    # Через некоторое время М отправляет пакет 3 повторно
    print("\n[M]: Sending packet again with delay")
    time.sleep(1)

    received_3_replay = transmit_packet(packet_3)
    result_3_fail = receiver_process_packet(SHARED_KEY, received_3_replay)
    print(f"result is : {'OK' if result_3_fail else 'FAILURE'}")


def main():
    # fair()
    # mim()
    reply()


if __name__ == "__main__":
    main()


# %% Cell
print("hello")