// UI helpers keep DOM manipulation away from crypto and simulation logic.
export function createUI() {
  const sharedKeyEl = document.getElementById("sharedKey");
  const logMap = {
    fair: document.getElementById("log-fair"),
    mitm: document.getElementById("log-mitm"),
    replay: document.getElementById("log-replay"),
    interactive: document.getElementById("log-interactive"),
  };
  const sequenceMap = {
    fair: document.querySelector("[data-sequence='fair']"),
    mitm: document.querySelector("[data-sequence='mitm']"),
    replay: document.querySelector("[data-sequence='replay']"),
    interactive: document.querySelector("[data-sequence='interactive']"),
  };
  const queues = Object.keys(logMap).reduce((acc, key) => {
    acc[key] = Promise.resolve();
    return acc;
  }, {});
  const actors = {};
  Object.entries(sequenceMap).forEach(([id, el]) => {
    if (!el) return;
    actors[id] = {
      A: el.querySelector("[data-actor='A']"),
      M: el.querySelector("[data-actor='M']"),
      B: el.querySelector("[data-actor='B']"),
    };
  });

  function setSharedKey(hex) {
    sharedKeyEl.textContent = hex;
  }

  function clearLog(id) {
    logMap[id].innerHTML = "";
    queues[id] = Promise.resolve();
  }

  function highlightActor(id, actor) {
    if (!actors[id]) return;
    Object.values(actors[id]).forEach((node) => node?.classList.remove("active"));
    const target = actors[id][actor];
    if (target) target.classList.add("active");
  }

  function wait(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  // sequential log with per-scenario queue to create delay between entries
  async function log(id, title, detail, status, options = {}) {
    const delay = options.delay ?? 950; // большее время, чтобы анимация была заметнее
    queues[id] = queues[id].then(async () => {
      if (options.actor) highlightActor(id, options.actor);

      const line = document.createElement("div");
      line.className = "log-line";
      if (options.actor === "A") line.classList.add("from-a");
      if (options.actor === "B") line.classList.add("from-b");
      if (options.actor === "M") line.classList.add("from-m");
      if (status === "ok") line.classList.add("ok");
      if (status === "fail" || status === "error") line.classList.add("fail");

      const actorEl = document.createElement("div");
      actorEl.className = "actor-pill";
      if (options.actor === "M") actorEl.classList.add("m");
      if (options.actor === "B") actorEl.classList.add("b");
      actorEl.textContent = options.actor ?? "•";

      const body = document.createElement("div");
      body.className = "log-body";

      const titleEl = document.createElement("strong");
      titleEl.textContent = title;
      if (status === "ok") titleEl.classList.add("status-ok");
      if (status === "fail") titleEl.classList.add("status-fail");

      const detailEl = document.createElement("span");
      detailEl.className = "mono";
      detailEl.textContent = detail;

      body.appendChild(titleEl);
      body.appendChild(detailEl);

      if (options.data) {
        const details = document.createElement("details");
        details.className = "log-details";
        const summary = document.createElement("summary");
        summary.textContent = "Детали";
        const pre = document.createElement("pre");
        pre.textContent = JSON.stringify(options.data, null, 2);
        details.appendChild(summary);
        details.appendChild(pre);
        body.appendChild(details);
      }

      const statusEl = document.createElement("div");
      statusEl.className = "status-chip";
      if (status === "ok") statusEl.classList.add("ok");
      else if (status === "fail") statusEl.classList.add("fail");
      statusEl.textContent = status ? status.toUpperCase() : "";

      line.appendChild(actorEl);
      line.appendChild(body);
      line.appendChild(statusEl);
      logMap[id].appendChild(line);
      // Оставляем позицию скролла, чтобы видеть анимацию появления, без прыжка к низу.
      await wait(delay);
    });
    return queues[id];
  }

  return { setSharedKey, log, clearLog, highlightActor };
}
