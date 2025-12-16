// DOM rendering helpers
export function renderTable(headers, rows, container) {
  const table = document.createElement("table");
  const thead = document.createElement("thead");
  const headRow = document.createElement("tr");
  headers.forEach((h) => {
    const th = document.createElement("th");
    th.textContent = h;
    headRow.appendChild(th);
  });
  thead.appendChild(headRow);
  table.appendChild(thead);

  const tbody = document.createElement("tbody");
  rows.forEach((row) => {
    const tr = document.createElement("tr");
    row.forEach((cell) => {
      const td = document.createElement("td");
      td.textContent = cell;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);

  container.innerHTML = "";
  container.appendChild(table);
}

export function renderChips(items, container, onClick) {
  container.innerHTML = "";
  items.forEach((text, idx) => {
    const chip = document.createElement("div");
    chip.className = "chip";
    chip.textContent = text;
    if (onClick) {
      chip.tabIndex = 0;
      chip.setAttribute("role", "button");
      chip.setAttribute("aria-label", `Point ${text}`);
      chip.addEventListener("click", () => onClick(idx));
      chip.addEventListener("keypress", (evt) => {
        if (evt.key === "Enter" || evt.key === " ") {
          evt.preventDefault();
          onClick(idx);
        }
      });
    }
    container.appendChild(chip);
  });
}
