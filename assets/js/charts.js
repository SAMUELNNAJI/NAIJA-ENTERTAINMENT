/**
 * Shared Chart.js helper.
 * Each chart canvas gets data-chart="line|bar|doughnut" and data-labels +
 * data-datasets JSON attributes.
 */
(function () {
  const CTX = window.Chart || null;

  function safeParse(str) {
    try { return JSON.parse(str); } catch (e) { return null; }
  }

  function render(id, type, labels, datasets) {
    const ctx = document.getElementById(id);
    if (!ctx) return;
    try {
      new CTX(ctx, {
        type: type,
        data: { labels: labels || [], datasets: datasets || [] },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: "bottom", labels: { color: "#e8e8f0", font: { size: 11 } } } },
          scales: {
            x: { ticks: { color: "#9a9ab0" }, grid: { color: "rgba(255,255,255,0.06)" } },
            y: { ticks: { color: "#9a9ab0" }, grid: { color: "rgba(255,255,255,0.06)" } },
          },
        },
      });
    } catch (e) {
      console.warn("Chart render failed for", id, e);
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    const cs = document.querySelectorAll("[data-chart]");
    cs.forEach(function (canvas) {
      const id = canvas.id || "chart-" + Math.random().toString(36).slice(2, 8);
      canvas.id = id;
      const type = canvas.getAttribute("data-chart");
      const from = canvas.getAttribute("data-from");
      let labels = [];
      let datasets = [];
      if (from) {
        const src = document.getElementById(from);
        if (src) {
          try {
            const data = JSON.parse(src.textContent || "{}");
            labels = data.labels || [];
            datasets = data.datasets || [];
          } catch (e) {
            console.warn("Chart JSON parse failed for", from, e);
          }
        }
      }
      render(id, type, labels, datasets);
    });
  });
})();
