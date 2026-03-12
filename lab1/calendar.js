function buildCalendar(root) {
  const label = root.querySelector("[data-cal-label]");
  const grid = root.querySelector("[data-cal-grid]");
  const prevBtn = root.querySelector("[data-cal-prev]");
  const nextBtn = root.querySelector("[data-cal-next]");

  if (!label || !grid || !prevBtn || !nextBtn) return;

  const today = new Date();
  const todayY = today.getFullYear();
  const todayM = today.getMonth();
  const todayD = today.getDate();

  const viewDate = new Date(today.getFullYear(), today.getMonth(), 1);

  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  function daysInMonth(year, monthIndex) {
    return new Date(year, monthIndex + 1, 0).getDate();
  }

  function render() {
    const year = viewDate.getFullYear();
    const month = viewDate.getMonth();

    label.textContent = `${monthNames[month]} ${year}`;
    grid.innerHTML = "";

    const startWeekdayIndex = new Date(year, month, 1).getDay(); 
    const totalDays = daysInMonth(year, month);
    const prevMonthDays = daysInMonth(year, month - 1);

    const totalCells = Math.ceil((startWeekdayIndex + totalDays) / 7) * 7;

    for (let i = 0; i < totalCells; i += 1) {
      const cell = document.createElement("div");
      cell.className = "day";
      cell.setAttribute("role", "gridcell");

      const dayNumber = i - startWeekdayIndex + 1;
      const isInMonth = dayNumber >= 1 && dayNumber <= totalDays;

      if (!isInMonth) {
        cell.classList.add("inactive");
        if (dayNumber < 1) {
          cell.textContent = String(prevMonthDays + dayNumber);
        } else {
          cell.textContent = String(dayNumber - totalDays);
        }
        cell.setAttribute("aria-hidden", "true");
        grid.appendChild(cell);
        continue;
      }

      cell.textContent = String(dayNumber);

      const isToday =
        year === todayY && month === todayM && dayNumber === todayD;
      if (isToday) {
        cell.classList.add("today");
        cell.setAttribute(
          "aria-label",
          `Today, ${monthNames[month]} ${dayNumber}`
        );
      } else {
        cell.setAttribute("aria-label", `${monthNames[month]} ${dayNumber}`);
      }

      grid.appendChild(cell);
    }
  }

  prevBtn.addEventListener("click", () => {
    viewDate.setMonth(viewDate.getMonth() - 1);
    viewDate.setDate(1);
    render();
  });

  nextBtn.addEventListener("click", () => {
    viewDate.setMonth(viewDate.getMonth() + 1);
    viewDate.setDate(1);
    render();
  });

  render();
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-calendar]").forEach((root) => {
    buildCalendar(root);
  });
});

