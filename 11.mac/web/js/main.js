import { createSimulation } from "./simulation.js";
import { createUI } from "./ui.js";

const ui = createUI();
const sim = createSimulation(ui);

// Инициализируем ключ и отображаем его.
ui.setSharedKey(sim.getKeyHex());

const grid = document.querySelector(".grid");
const cards = Array.from(document.querySelectorAll(".card"));
let focusMode = false;
let activeScenario = cards[0]?.dataset.scenario;

function setActiveScenario(name) {
  activeScenario = name;
  cards.forEach((card) => {
    const isActive = card.dataset.scenario === name;
    card.classList.toggle("active", isActive);
  });
}

function setFocusMode(enabled) {
  focusMode = enabled;
  grid.classList.toggle("focus-mode", enabled);
  document.getElementById("focusToggle").textContent = `Режим фокуса: ${enabled ? "вкл" : "выкл"}`;
  if (enabled && activeScenario) setActiveScenario(activeScenario);
  if (!enabled) cards.forEach((card) => card.classList.remove("active"));
}

document.querySelectorAll("[data-action='run']").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const target = btn.dataset.target;
    setActiveScenario(target);
    btn.disabled = true;
    btn.textContent = "Выполняется...";
    try {
      let options = {};
      if (target === "interactive") {
        options = {
          original: document.getElementById("origMessage").value || "Command: Sync backup",
          tampered: document.getElementById("tamperMessage").value || "Command: Delete audit log",
          doTamper: document.getElementById("tamperToggle").checked,
        };
      }
      await sim.runScenario(target, options);
    } catch (err) {
      console.error(err);
      ui.log(target, "Ошибка", err.message, "fail");
    } finally {
      btn.disabled = false;
      btn.textContent = "Запустить";
    }
  });
});

const resetBtn = document.getElementById("resetKey");
resetBtn.addEventListener("click", () => {
  sim.resetKey();
});

const focusToggle = document.getElementById("focusToggle");
focusToggle.addEventListener("click", () => {
  setFocusMode(!focusMode);
});

cards.forEach((card) => {
  card.addEventListener("click", (evt) => {
    if (!focusMode) return;
    // не трогаем клики по кнопкам внутри
    if (evt.target.closest("button")) return;
    setActiveScenario(card.dataset.scenario);
  });
});

// Устанавливаем стартовое состояние.
setFocusMode(false);
