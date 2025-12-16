const createEl = (tag, className, text) => {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text !== undefined) el.textContent = text;
  return el;
};

const statusLabels = {
  ok: 'OK',
  warn: 'FAIL',
  info: 'INFO'
};

const renderLogLine = (line) => {
  const actorClass = line.actorClass || '';
  const lineClass = line.lineClass || '';
  const details = line.details
    ? `<details class="log-details"><summary>Детали</summary><pre>${line.details}</pre></details>`
    : '';
  const meta = line.meta?.length
    ? `<div class="stage__meta">${line.meta.map((m) => `<span class="meta-chip">${m}</span>`).join('')}</div>`
    : '';
  const status = line.status
    ? `<div class="status-chip ${line.status}">${statusLabels[line.status] || line.status}</div>`
    : '<div class="status-chip info"></div>';
  const chipStyle = line.color ? `style="background: radial-gradient(circle at 20% 20%, ${line.color}, #0c1420)"` : '';

  return `
    <div class="log-line ${lineClass}${line.from ? ` from-${line.from}` : ''} ${line.status ? `line-${line.status}` : ''}">
      <div class="actor-pill ${actorClass}" ${chipStyle}>${line.badge || '•'}</div>
      <div class="log-body">
        <strong>${line.title || ''}</strong>
        ${line.desc ? `<span class="mono">${line.desc}</span>` : ''}
        ${details}
        ${meta}
      </div>
      ${status}
    </div>
  `;
};

const renderStageCard = (stage) => {
  const badgeBg = stage.color
    ? `radial-gradient(circle at 20% 20%, ${stage.color}, #0c1420)`
    : 'rgba(255, 255, 255, 0.06)';
  const status = stage.status
    ? `<span class="stage__status stage__status--${stage.status}">${statusLabels[stage.status] || stage.status}</span>`
    : '';
  const formulas = stage.formulas?.length
    ? stage.formulas.map((f) => `<div class="stage__formula mono">${f}</div>`).join('')
    : '';
  const meta = stage.meta?.length
    ? `<div class="stage__meta">${stage.meta.map((m) => `<span class="meta-chip">${m}</span>`).join('')}</div>`
    : '';

  return `
    <div class="stage-card fade-in">
      <div class="stage__badge" style="background:${badgeBg}">${stage.badge || ''}</div>
      <div class="stage__body">
        <div class="stage__title">
          <div class="stage__headline">${stage.title || ''}</div>
          ${status}
        </div>
        ${stage.desc ? `<div class="stage__desc">${stage.desc}</div>` : ''}
        ${formulas}
        ${meta}
      </div>
    </div>
  `;
};

export const renderPublicParams = (params) => {
  const el = document.getElementById('public-params');
  el.textContent = `P=${params.P} • G=${params.G}`;
};

export const renderCircle = (users, onSelect, selectedName) => {
  const container = document.getElementById('circle');
  container.innerHTML = '';
  const radius = 42;
  const center = { x: 50, y: 50 };

  users.forEach((user, idx) => {
    const angle = (2 * Math.PI * idx) / users.length;
    const x = center.x + radius * Math.cos(angle);
    const y = center.y + radius * Math.sin(angle);

    const node = createEl('div', 'user-node', user.name);
    node.style.left = `${x}%`;
    node.style.top = `${y}%`;
    node.style.transform = 'translate(-50%, -50%)';
    node.style.background = `radial-gradient(circle at 20% 20%, ${user.color}, #0c1420)`;
    if (user.name === selectedName) node.classList.add('active');
    node.addEventListener('click', () => onSelect(user));
    container.appendChild(node);
  });
};

export const renderSelectedUser = (user) => {
  const el = document.getElementById('selected-user');
  if (!user) {
    el.textContent = 'Нажмите на участника, чтобы увидеть его публичный ключ и отправить сообщение.';
    return;
  }
  el.innerHTML = `
    <div class="chip"><span class="color-dot" style="background:${user.color}"></span><strong>${user.name}</strong></div>
    <span class="mono">Public: ${user.publicKey}</span>
  `;
};

export const renderKeyTable = (users, params) => {
  const container = document.getElementById('key-table');
  const table = document.createElement('table');
  const head = document.createElement('thead');
  head.innerHTML = `
    <tr>
      <th>Абонент</th>
      <th>Секрет</th>
      <th>Публичный ключ</th>
    </tr>
  `;
  const body = document.createElement('tbody');
  users.forEach((u) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${u.name}</td>
      <td class="mono">${u.secret}</td>
      <td class="mono">${u.publicKey}</td>
    `;
    body.appendChild(row);
  });
  table.appendChild(head);
  table.appendChild(body);
  container.innerHTML = '';
  container.appendChild(table);
};

export const populateSelect = (select, users, excludeName) => {
  select.innerHTML = '';
  users.forEach((u) => {
    if (u.name === excludeName) return;
    const opt = createEl('option');
    opt.value = u.name;
    opt.textContent = u.name;
    select.appendChild(opt);
  });
};

export const renderExchangeLog = (result) => {
  const log = document.getElementById('exchange-log');
  log.classList.add('stage-log', 'stacked-log');
  if (!result) {
    log.innerHTML = renderLogLine({
      badge: 'ℹ',
      actorClass: 'info',
      title: 'Журнал обмена',
      desc: 'Выберите двух абонентов и нажмите «Выполнить обмен».',
      status: 'info'
    });
    return;
  }
  if (result.error) {
    log.innerHTML = renderLogLine({ badge: '!', actorClass: 'm', title: 'Ошибка', desc: result.error, status: 'warn' });
    return;
  }
  if (!result.details) {
    const html = result.steps.map((line) => `<span>• ${line}</span>`).join('<br>');
    log.innerHTML = html;
    return;
  }

  const { sender, receiver, params, calculations } = result.details;
  const lines = [
    {
      badge: 'P,G',
      actorClass: 'p',
      title: 'Общие параметры',
      desc: 'Публично известны и одинаковы для всех.',
      meta: [`P=${params.P}`, `G=${params.G}`],
      status: 'info'
    },
    {
      badge: sender.name,
      actorClass: 'a',
      lineClass: 'from-a',
      from: 'a',
      title: `Открытый ключ ${sender.name}`,
      desc: `Секрет ${sender.secret} сохраняется в тайне.`,
      details: calculations.senderPublic,
      status: 'info',
      color: sender.color
    },
    {
      badge: receiver.name,
      actorClass: 'b',
      lineClass: 'from-b',
      from: 'b',
      title: `Открытый ключ ${receiver.name}`,
      desc: `Секрет ${receiver.secret} хранится у ${receiver.name}.`,
      details: calculations.receiverPublic,
      status: 'info',
      color: receiver.color
    },
    {
      badge: sender.name,
      actorClass: 'a',
      lineClass: 'from-a',
      from: 'a',
      title: `Общий ключ у ${sender.name}`,
      desc: `Использует публичный ключ ${receiver.name}.`,
      details: calculations.senderShared,
      meta: [`Ключ = ${result.sharedSender}`],
      status: result.match ? 'ok' : 'warn',
      color: sender.color
    },
    {
      badge: receiver.name,
      actorClass: 'b',
      lineClass: 'from-b',
      from: 'b',
      title: `Общий ключ у ${receiver.name}`,
      desc: `Использует публичный ключ ${sender.name}.`,
      details: calculations.receiverShared,
      meta: [`Ключ = ${result.sharedReceiver}`],
      status: result.match ? 'ok' : 'warn',
      color: receiver.color
    },
    {
      badge: 'Σ',
      actorClass: 'info',
      title: result.match ? 'Ключи совпали' : 'Ключи не совпали',
      desc: result.match ? `Shared = ${result.sharedSender}` : 'Передача сообщения невозможна — выберите других участников.',
      status: result.match ? 'ok' : 'warn'
    }
  ];

  log.innerHTML = lines.map(renderLogLine).join('');
};

export const renderWire = (payload) => {
  const wire = document.getElementById('wire-preview');
  if (!payload) {
    wire.textContent = 'Шифротекст появится здесь после отправки.';
    return;
  }
  wire.innerHTML = `
    <div class="chip"><strong>На проводе</strong> <span class="mono">${payload.cipher}</span></div>
    <div class="chip"><strong>Ключ</strong> <span class="mono">${payload.key}</span></div>
    <div class="chip"><strong>Расшифровка</strong> ${payload.plain || 'Без текста'}</div>
  `;
};

export const renderMitmLog = (data) => {
  const log = document.getElementById('mitm-log');
  log.classList.add('stage-log', 'stacked-log');
  if (!data) {
    log.innerHTML = renderLogLine({
      badge: 'ℹ',
      actorClass: 'info',
      title: 'Подмена сообщений',
      desc: 'Выберите пару жертв и запустите сценарий, чтобы увидеть этапы атаки.',
      status: 'info'
    });
    return;
  }
  // MITM лог теперь рисуется в таймлайне, этот блок оставляем для краткого резюме.
  const { victimA, victimB } = data.parties;
  log.innerHTML = renderLogLine({
    badge: 'Σ',
    actorClass: 'info',
    title: 'Сводка MITM',
    desc: `Сообщение от ${victimA.name} уходит к ${victimB.name} через атакующего. Ключи: ${data.shared.victimA} / ${data.shared.victimB}`,
    status: 'info',
    meta: [`Шифр: ${data.wire.fromVictim}`, `Подмена: ${data.wire.toVictim}`]
  });
};

export const renderMitmTimeline = (state) => {
  const timeline = document.getElementById('mitm-timeline');
  timeline.classList.add('stacked-log');
  if (!state) {
    timeline.innerHTML = renderLogLine({
      badge: 'ℹ',
      actorClass: 'info',
      title: 'Атака не запущена',
      desc: 'Нажмите «Запустить симуляцию», чтобы увидеть перехват.',
      status: 'info'
    });
    return;
  }
  const { victimA, victimB, attacker } = state.parties;
  const { P, G } = state.publicParams;
  const secrets = state.secrets || {};
  const lines = [
    {
      badge: 'P,G',
      actorClass: 'p',
      title: 'Параметры сети',
      desc: 'Публичные числа одинаковы для всех.',
      meta: [`P=${P}`, `G=${G}`],
      status: 'info'
    },
    {
      badge: victimA.name,
      actorClass: 'a',
      lineClass: 'from-a',
      from: 'a',
      title: 'Подмена публичных ключей',
      desc: `${victimA.name} и ${victimB.name} получают подмененные значения.`,
      details: [
        `${victimA.name}: g^${secrets.attackerA} mod ${P} = ${state.attackerPublic.toA}`,
        `${victimB.name}: g^${secrets.attackerB} mod ${P} = ${state.attackerPublic.toB}`
      ].join('\n'),
      meta: [`Public ${victimA.name}: ${state.victimPublic?.a}`, `Public ${victimB.name}: ${state.victimPublic?.b}`],
      status: 'warn'
    },
    {
      badge: victimA.name,
      actorClass: 'a',
      lineClass: 'from-a',
      from: 'a',
      title: 'Шифрование жертвы',
      desc: `Текст: "${state.plain.sentByA}"`,
      details: `ENC(m, ${state.shared.victimA}) = ${state.wire.fromVictim}`,
      meta: [`Ключ ${victimA.name}: ${state.shared.victimA}`],
      status: 'info'
    }
  ];

  // Интерсепт карточка
  const interceptButtons = `
    <div class="intercept__controls">
      <button class="pill-btn ghost" data-action="mitm-skip" ${state.forwarded ? 'disabled' : ''}>Пропустить</button>
      <button class="pill-btn primary" data-action="mitm-decrypt" ${state.decrypted || state.forwarded ? 'disabled' : ''}>Расшифровать</button>
      ${state.decrypted && !state.forwarded ? '<button class="pill-btn primary" data-action="mitm-send">Отправить</button>' : ''}
    </div>
    ${state.decrypted && !state.forwarded ? `<textarea id="mitm-inline-edit" class="intercept__edit" rows="2">${state.forgedText || ''}</textarea>` : ''}
  `;

  const interceptHTML = `
    <div class="log-line from-m intercept">
      <div class="actor-pill m">${attacker.name[0] || 'M'}</div>
      <div class="log-body">
        <strong>Перехват сообщения</strong>
        <div class="intercept__cipher mono">${state.wire.fromVictim}</div>
        ${state.decrypted ? `<div class="mono">Текст: "${state.plain.seenByAttacker}"</div>` : ''}
        ${interceptButtons}
      </div>
      <div class="status-chip ${state.forwarded ? 'ok' : 'warn'}">${state.forwarded ? 'OK' : 'WAIT'}</div>
    </div>
  `;

  const tail = [];
  if (state.forwarded) {
    tail.push({
      badge: victimB.name,
      actorClass: 'b',
      lineClass: 'from-b',
      from: 'b',
      title: 'Отправлено получателю',
      desc: `Шифр: ${state.wire.toVictim}`,
      details: `DEC(${state.wire.toVictim}, ${state.shared.victimB}) = "${state.plain.deliveredToB}"`,
      meta: [`Ключ ${victimB.name}: ${state.shared.victimB}`],
      status: 'ok'
    });
  }

  timeline.innerHTML = `${lines.map(renderLogLine).join('')}${interceptHTML}${tail.map(renderLogLine).join('')}`;
};
