/**
 * Shared Chart.js helper for Creator Studio & Admin Command Center.
 * Reads JSON configuration from <script type="application/json"> data sources.
 */
(function () {
  const CTX = window.Chart || null;

  function render(id, type, labels, datasets) {
    const ctx = document.getElementById(id);
    if (!ctx || !CTX) return;

    const isDark = document.documentElement.getAttribute("data-theme") !== "light";
    const textColor = isDark ? "#94a3b8" : "#64748b";
    const gridColor = isDark ? "rgba(255, 255, 255, 0.05)" : "rgba(15, 23, 42, 0.06)";

    const options = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: type === "doughnut" || type === "pie",
          position: "bottom",
          labels: {
            color: textColor,
            font: { family: "'Plus Jakarta Sans', sans-serif", size: 11, weight: "600" },
            padding: 14,
            usePointStyle: true,
            boxWidth: 8,
          },
        },
        tooltip: {
          backgroundColor: isDark ? "rgba(13, 20, 36, 0.95)" : "rgba(255, 255, 255, 0.95)",
          titleColor: isDark ? "#f8fafc" : "#0f172a",
          bodyColor: isDark ? "#cbd5e1" : "#334155",
          borderColor: isDark ? "rgba(255, 255, 255, 0.1)" : "rgba(15, 23, 42, 0.1)",
          borderWidth: 1,
          padding: 10,
          cornerRadius: 10,
          boxPadding: 4,
          usePointStyle: true,
        },
      },
    };

    if (type !== "doughnut" && type !== "pie") {
      options.scales = {
        x: {
          ticks: {
            color: textColor,
            font: { family: "'Plus Jakarta Sans', sans-serif", size: 10.5, weight: "600" },
            maxRotation: 0,
            autoSkip: true,
            maxTicksLimit: 7,
          },
          grid: { color: gridColor },
        },
        y: {
          ticks: {
            color: textColor,
            font: { family: "'Plus Jakarta Sans', sans-serif", size: 10.5, weight: "600" },
            precision: 0,
          },
          grid: { color: gridColor },
          beginAtZero: true,
        },
      };
    } else {
      options.cutout = "68%";
    }

    try {
      new CTX(ctx, {
        type: type,
        data: { labels: labels || [], datasets: datasets || [] },
        options: options,
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
