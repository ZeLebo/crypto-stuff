import { generatePublicParams } from './crypto.js';
import { buildUsers, buildAttacker } from './userFactory.js';
import { runExchange } from './exchange.js';
import { encryptMessage, decryptMessage } from './cipher.js';
import { runMitmScenario } from './attackSimulation.js';
import { createLogState, pushLog, getLog } from './messageLog.js';
import {
  renderCircle,
  renderKeyTable,
  renderSelectedUser,
  renderPublicParams,
  populateSelect,
  renderExchangeLog,
  renderWire,
  renderMitmLog,
  renderMitmTimeline
} from './ui.js';

const state = {
  params: null,
  users: [],
  attacker: null,
  selected: null,
  exchangeResult: null,
  messageLog: {},
  mitmSession: null,
  userCount: 6
};

const init = () => {
  state.params = generatePublicParams();
  state.users = buildUsers(state.userCount, state.params);
  state.attacker = buildAttacker(state.params);
  state.selected = null;
  state.exchangeResult = null;
  state.messageLog = createLogState(state.users);
  state.mitmSession = null;
  render();
};

const render = () => {
  renderPublicParams(state.params);
  renderCircle(state.users, handleSelectUser, state.selected?.name);
  renderSelectedUser(state.selected);
  renderKeyTable(state.users, state.params);
  populateSelect(document.getElementById('sender'), state.users);
  populateSelect(document.getElementById('receiver'), state.users);
  populateMitmPairs();
  renderExchangeLog(state.exchangeResult);
  renderWire(null);
  renderMitmLog(null);
  renderMitmTimeline(null);
  renderSelectedLog();
  document.getElementById('user-count').value = state.userCount;
  document.getElementById('mitm-edit').classList.add('hidden');
  const runMitmBtn = document.getElementById('run-mitm');
  if (runMitmBtn) runMitmBtn.textContent = 'Запустить симуляцию';
  const reveal = document.getElementById('reveal-mitm');
  const forward = document.getElementById('forward-mitm');
  if (reveal) reveal.style.display = 'none';
  if (forward) forward.style.display = 'none';
};

const populateMitmPairs = () => {
  const select = document.getElementById('mitm-pair');
  select.innerHTML = '';
  state.users.forEach((u, idx) => {
    const next = state.users[(idx + 1) % state.users.length];
    const opt = document.createElement('option');
    opt.value = `${u.name},${next.name}`;
    opt.textContent = `${u.name} ↔ ${next.name}`;
    select.appendChild(opt);
  });
};

const handleSelectUser = (user) => {
  state.selected = user;
  renderCircle(state.users, handleSelectUser, user.name);
  renderSelectedUser(user);
  populateSelect(document.getElementById('receiver'), state.users);
  document.getElementById('receiver').value = state.selected.name;
  renderSelectedLog();
};

const handleExchange = () => {
  const senderName = document.getElementById('sender').value;
  const receiverName = document.getElementById('receiver').value;
  const message = document.getElementById('message').value || 'Без текста';

  if (senderName === receiverName) {
    renderExchangeLog({ error: 'Нужно выбрать двух разных абонентов' });
    renderWire(null);
    return;
  }

  const sender = state.users.find((u) => u.name === senderName);
  const receiver = state.users.find((u) => u.name === receiverName);
  state.exchangeResult = runExchange(sender, receiver, state.params);
  renderExchangeLog(state.exchangeResult);

  if (state.exchangeResult.match) {
    const cipher = encryptMessage(message, state.exchangeResult.shared);
    const plain = decryptMessage(cipher, state.exchangeResult.shared);
    renderWire({ cipher, key: state.exchangeResult.shared, plain });
    pushLog(state.messageLog, sender.name, {
      from: sender.name,
      to: receiver.name,
      cipher,
      plain,
      key: state.exchangeResult.shared,
      direction: 'sent'
    });
    pushLog(state.messageLog, receiver.name, {
      from: sender.name,
      to: receiver.name,
      cipher,
      plain,
      key: state.exchangeResult.shared,
      direction: 'received'
    });
    renderSelectedLog();
  } else {
    renderWire(null);
  }
};

const handleMitm = () => {
  const value = document.getElementById('mitm-pair').value;
  const [aName, bName] = value.split(',');
  const victimA = state.users.find((u) => u.name === aName);
  const victimB = state.users.find((u) => u.name === bName);
  const text = document.getElementById('mitm-message').value;

  const result = runMitmScenario(victimA, victimB, state.attacker, state.params, text);
  state.mitmSession = {
    ...result,
    revealed: false,
    decrypted: false,
    forwarded: false,
    forgedText: result.plain.sentByA
  };
  state.mitmSession.plain.seenByAttacker = 'скрыто до расшифровки';
  state.mitmSession.wire.toVictim = '(ждет отправки)';
  state.mitmSession.plain.deliveredToB = '(ждет отправки)';
  document.getElementById('mitm-forged').value = state.mitmSession.forgedText;
  renderMitmLog(state.mitmSession);
  renderMitmTimeline(state.mitmSession);
};

const handleMitmDecrypt = () => {
  if (!state.mitmSession || state.mitmSession.forwarded) return;
  const plain = decryptMessage(state.mitmSession.wire.fromVictim, state.mitmSession.shared.attackerWithA);
  state.mitmSession.decrypted = true;
  state.mitmSession.revealed = true;
  state.mitmSession.plain.seenByAttacker = plain;
  state.mitmSession.forgedText = plain;
  renderMitmTimeline(state.mitmSession);
  renderMitmLog(state.mitmSession);
};

const handleMitmSkip = () => {
  if (!state.mitmSession || state.mitmSession.forwarded) return;
  const cipherToB = state.mitmSession.wire.fromVictim;
  const delivered = decryptMessage(cipherToB, state.mitmSession.shared.victimB);
  state.mitmSession.forwarded = true;
  state.mitmSession.wire.toVictim = cipherToB;
  state.mitmSession.plain.deliveredToB = delivered;
  renderMitmTimeline(state.mitmSession);
  renderMitmLog(state.mitmSession);
  const { victimA, victimB } = state.mitmSession.parties;
  pushLog(state.messageLog, victimA.name, {
    from: victimA.name,
    to: victimB.name,
    cipher: state.mitmSession.wire.fromVictim,
    plain: state.mitmSession.plain.sentByA,
    key: state.mitmSession.shared.victimA,
    direction: 'sent'
  });
  pushLog(state.messageLog, victimB.name, {
    from: victimA.name,
    to: victimB.name,
    cipher: cipherToB,
    plain: delivered,
    key: state.mitmSession.shared.victimB,
    direction: 'received'
  });
  renderSelectedLog();
};

const handleMitmSend = () => {
  if (!state.mitmSession || state.mitmSession.forwarded) return;
  const newText = state.mitmSession.forgedText || '(пусто)';
  const cipherToB = encryptMessage(newText, state.mitmSession.shared.attackerWithB);
  const delivered = decryptMessage(cipherToB, state.mitmSession.shared.victimB);
  state.mitmSession.forwarded = true;
  state.mitmSession.wire.toVictim = cipherToB;
  state.mitmSession.plain.deliveredToB = delivered;
  state.mitmSession.plain.seenByAttacker = newText;
  renderMitmTimeline(state.mitmSession);
  renderMitmLog(state.mitmSession);
  const { victimA, victimB } = state.mitmSession.parties;
  pushLog(state.messageLog, victimA.name, {
    from: victimA.name,
    to: victimB.name,
    cipher: state.mitmSession.wire.fromVictim,
    plain: state.mitmSession.plain.sentByA,
    key: state.mitmSession.shared.victimA,
    direction: 'sent'
  });
  pushLog(state.messageLog, victimB.name, {
    from: victimA.name,
    to: victimB.name,
    cipher: cipherToB,
    plain: delivered,
    key: state.mitmSession.shared.victimB,
    direction: 'received'
  });
  renderSelectedLog();
};

const renderSelectedLog = () => {
  const target = document.getElementById('selected-user');
  const existing = target.querySelector('.log-list');
  if (existing) existing.remove();
  const list = document.createElement('div');
  list.className = 'log-list';
  const user = state.selected;
  if (!user) return;
  const logs = getLog(state.messageLog, user.name);
  if (!logs.length) {
    const empty = document.createElement('div');
    empty.className = 'log-card';
    empty.textContent = 'Сообщения этого абонента появятся здесь.';
    list.appendChild(empty);
  }
  logs.slice(-5).reverse().forEach((entry) => {
    const card = document.createElement('div');
    card.className = 'log-card fade-in';
    const label = entry.direction === 'sent' ? `Отправлено: ${entry.to}` : `Получено: ${entry.from}`;
    card.innerHTML = `
      <strong>${label}</strong>
      <span class="mono">Шифр: ${entry.cipher}</span>
      <span class="mono">Ключ: ${entry.key}</span>
      <span>Текст: ${entry.plain}</span>
    `;
    list.appendChild(card);
  });
  target.appendChild(list);
};

const handleUserCount = () => {
  const value = Number(document.getElementById('user-count').value);
  if (!Number.isInteger(value) || value < 2 || value > 16) return;
  state.userCount = value;
  init();
};

document.addEventListener('DOMContentLoaded', () => {
  init();
  document.getElementById('run-exchange').addEventListener('click', handleExchange);
  document.getElementById('run-mitm').addEventListener('click', handleMitm);
  document.getElementById('regenerate').addEventListener('click', init);
  document.getElementById('apply-count').addEventListener('click', handleUserCount);
  document.getElementById('mitm-timeline').addEventListener('click', (e) => {
    const action = e.target.dataset.action;
    if (action === 'mitm-decrypt') handleMitmDecrypt();
    if (action === 'mitm-skip') handleMitmSkip();
    if (action === 'mitm-send') handleMitmSend();
  });
  document.getElementById('mitm-timeline').addEventListener('input', (e) => {
    if (e.target.id === 'mitm-inline-edit' && state.mitmSession) {
      state.mitmSession.forgedText = e.target.value;
    }
  });
});
