import { hmacSha256 } from "./hmac.js";
import { concatBytes, constantTimeEqual, fromString, randomBytes, toHex } from "./utils.js";

// Handles packet creation/verification and scenarios; UI interactions are injected.
export function createSimulation(ui) {
  let sharedKey = randomBytes(32);
  const usedNonces = new Set();

  function refreshKey() {
    sharedKey = randomBytes(32);
    usedNonces.clear();
    ui.setSharedKey(toHex(sharedKey));
  }

  async function createPacket(messageText) {
    const messageBytes = fromString(messageText);
    const nonce = randomBytes(16);
    const mac = await hmacSha256(sharedKey, concatBytes(messageBytes, nonce));
    return { messageBytes, nonce, mac, messageText };
  }

  function transmit(packet) {
    // Прозрачная передача по каналу; здесь просто возвращаем то же содержимое.
    return { ...packet };
  }

  async function verifyPacket(packet, { showDiff } = {}) {
    const packetNonceHex = toHex(packet.nonce);
    const dataToCheck = concatBytes(packet.messageBytes, packet.nonce);
    const expectedMac = await hmacSha256(sharedKey, dataToCheck);
    const receivedMac = packet.mac;
    const isValid = constantTimeEqual(expectedMac, receivedMac);

    await ui.log(
      packet.scenario,
      "B · получен пакет",
      `Nonce ${packetNonceHex.slice(0, 8)}...`,
      "info",
      {
        actor: "B",
        data: {
          message: packet.messageText,
          nonce: packetNonceHex,
          mac: toHex(receivedMac),
          expectedMac: showDiff ? toHex(expectedMac) : undefined,
        },
      }
    );

    if (usedNonces.has(packetNonceHex)) {
      await ui.log(packet.scenario, "B · отклонение", "Nonce уже использован (replay).", "fail", {
        actor: "B",
      });
      return false;
    }

    if (isValid) {
      usedNonces.add(packetNonceHex);
      await ui.log(
        packet.scenario,
        "B · подпись верна",
        "MAC совпадает, Nonce помечен как использованный.",
        "ok",
        {
          actor: "B",
          data: showDiff
            ? {
                expectedMac: toHex(expectedMac),
                receivedMac: toHex(receivedMac),
              }
            : undefined,
        }
      );
    } else {
      await ui.log(
        packet.scenario,
        "B · подпись неверна",
        showDiff
          ? `MAC не совпадает: ожидалось ${toHex(expectedMac).slice(0, 16)}..., пришло ${toHex(
              receivedMac
            ).slice(0, 16)}...`
          : "MAC не совпадает: данные подменены.",
        "fail",
        {
          actor: "B",
          data: {
            expectedMac: toHex(expectedMac),
            receivedMac: toHex(receivedMac),
          },
        }
      );
    }
    return isValid;
  }

  async function runFair() {
    usedNonces.clear();
    ui.clearLog("fair");
    await ui.log("fair", "A · подготовка", "Команда: Sync backup", "info", {
      actor: "A",
    });

    const packet = await createPacket("Command: Sync backup");
    const packetHex = toHex(packet.mac).slice(0, 16);
    await ui.log("fair", "A · MAC создан", `Tag ${packetHex}...`, "ok", {
      actor: "A",
      data: {
        message: packet.messageText,
        nonce: toHex(packet.nonce),
        mac: toHex(packet.mac),
      },
    });

    packet.scenario = "fair";
    const delivered = transmit(packet);
    const ok = await verifyPacket(delivered, { showDiff: false });

    await ui.log(
      "fair",
      ok ? "✓ Достоверно" : "✕ Ошибка",
      ok ? "Сообщение принято." : "Не удалось подтвердить.",
      ok ? "ok" : "fail",
      { actor: "B" }
    );
  }

  async function runMitm() {
    usedNonces.clear();
    ui.clearLog("mitm");
    await ui.log("mitm", "A · подготовка", "Команда: Retrieve audit log", "info", {
      actor: "A",
    });
    const packet = await createPacket("Command: Retrieve audit log");
    await ui.log("mitm", "A · MAC создан", `Tag ${toHex(packet.mac).slice(0, 16)}...`, "ok", {
      actor: "A",
      data: {
        message: packet.messageText,
        nonce: toHex(packet.nonce),
        mac: toHex(packet.mac),
      },
    });

    const attackerText = "Command: Delete audit log";
    const attackerMessage = fromString(attackerText);

    await ui.log("mitm", "M · перехват", "Пакет перехвачен, готовим подмену.", "info", {
      actor: "M",
    });
    await ui.log("mitm", "M · подмена", "Сообщение изменено, MAC оставлен старый.", "fail", {
      actor: "M",
      data: { newMessage: attackerText, reusedMac: toHex(packet.mac) },
    });

    const tampered = {
      ...packet,
      messageBytes: attackerMessage,
      messageText: attackerText,
      scenario: "mitm",
    };
    const delivered = transmit(tampered);
    const ok = await verifyPacket(delivered, { showDiff: true });

    await ui.log(
      "mitm",
      ok ? "✓ Достоверно" : "✕ Подмена",
      ok ? "Сработало (неожиданно)." : "MAC не совпал — атака не удалась.",
      ok ? "ok" : "fail",
      { actor: "B" }
    );
  }

  async function runReplay() {
    usedNonces.clear();
    ui.clearLog("replay");
    await ui.log("replay", "A · подготовка", "Команда: Check balance", "info", {
      actor: "A",
    });
    const packet = await createPacket("Request: Check balance");
    packet.scenario = "replay";
    await ui.log("replay", "A · MAC создан", `Tag ${toHex(packet.mac).slice(0, 16)}...`, "ok", {
      actor: "A",
      data: {
        message: packet.messageText,
        nonce: toHex(packet.nonce),
        mac: toHex(packet.mac),
      },
    });

    await ui.log("replay", "M · перехват", "Пакет сохранён злоумышленником для повтора.", "info", {
      actor: "M",
      data: {
        message: packet.messageText,
        nonce: toHex(packet.nonce),
        mac: toHex(packet.mac),
      },
    });

    const firstDelivery = transmit(packet);
    const okFirst = await verifyPacket(firstDelivery, { showDiff: true });
    await ui.log(
      "replay",
      okFirst ? "✓ Принято" : "✕ Ошибка",
      okFirst ? "Первый пакет принят." : "Первый пакет отклонен.",
      okFirst ? "ok" : "fail",
      { actor: "B" }
    );
    await ui.log("replay", "M · повтор", "Отправляем старый пакет повторно без изменений.", "info", {
      actor: "M",
      data: {
        message: packet.messageText,
        nonce: toHex(packet.nonce),
        mac: toHex(packet.mac),
      },
    });
    const replayDelivery = transmit(packet);
    const okReplay = await verifyPacket(replayDelivery, { showDiff: true });
    await ui.log(
      "replay",
      okReplay ? "✓ Принято" : "✕ Отклонено",
      okReplay ? "Повтор неожиданно принят." : "Nonce уже был — повтор отвергнут.",
      okReplay ? "ok" : "fail",
      { actor: "B" }
    );
  }

  async function runInteractive(options) {
    usedNonces.clear();
    ui.clearLog("interactive");

    const original = options.original || "Command: Sync backup";
    const tampered = options.tampered || original;
    const doTamper = Boolean(options.doTamper);

    await ui.log("interactive", "A · подготовка", original, "info", { actor: "A" });
    const packet = await createPacket(original);
    packet.scenario = "interactive";
    await ui.log(
      "interactive",
      "A · MAC создан",
      `Tag ${toHex(packet.mac).slice(0, 16)}...`,
      "ok",
      {
        actor: "A",
        data: {
          message: packet.messageText,
          nonce: toHex(packet.nonce),
          mac: toHex(packet.mac),
        },
      }
    );

    let outgoing = packet;
    if (doTamper) {
      const tamperBytes = fromString(tampered);
      outgoing = {
        ...packet,
        messageBytes: tamperBytes,
        messageText: tampered,
      };
      await ui.log(
        "interactive",
        "Вы · подмена",
        "Сообщение изменено, MAC оставлен прежний.",
        "fail",
        {
          actor: "M",
          data: { newMessage: tampered, reusedMac: toHex(packet.mac) },
        }
      );
    } else {
      await ui.log("interactive", "Вы · без подмены", "Пакет проходит как есть.", "info", {
        actor: "M",
      });
    }

    const delivered = transmit(outgoing);
    const okFirst = await verifyPacket(delivered, { showDiff: true });
    await ui.log(
      "interactive",
      okFirst ? "✓ Результат" : "✕ Ошибка",
      okFirst ? "Пакет принят." : "Пакет отклонён.",
      okFirst ? "ok" : "fail",
      { actor: "B" }
    );

  }

  async function runScenario(name, options = {}) {
    if (name === "fair") return runFair();
    if (name === "mitm") return runMitm();
    if (name === "replay") return runReplay();
    if (name === "interactive") return runInteractive({
      original: options.original,
      tampered: options.tampered,
      doTamper: options.doTamper,
    });
    throw new Error(`Unknown scenario: ${name}`);
  }

  return {
    runScenario,
    resetKey: refreshKey,
    getKeyHex: () => toHex(sharedKey),
  };
}
