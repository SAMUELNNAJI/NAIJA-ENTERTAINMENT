/* Local, persistent watchlist interactions for the market board. */
(function () {
  "use strict";
  const KEY = "tne-markets-2";
  const getList = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (_) { return []; } };
  const saveList = list => { try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (_) {} };

  document.addEventListener("DOMContentLoaded", () => {
    const count = document.querySelector("#count");
    const last = document.querySelector("#last");
    const source = document.querySelector("#market-source");
    const board = document.querySelector(".market-board[data-snapshot-url]");
    const rows = [...document.querySelectorAll("tr[data-symbol]")];
    const search = document.querySelector("#q");
    const empty = document.querySelector("#empty");
    let list = getList();
    const render = () => {
      count.textContent = list.length;
      rows.forEach(row => {
        const watched = list.includes(row.dataset.symbol);
        row.classList.toggle("is-watched", watched);
        const button = row.querySelector("[data-add]");
        button.textContent = watched ? "✓ Watching" : "+ Watch";
        button.setAttribute("aria-label", `${watched ? "Remove" : "Add"} ${row.dataset.symbol} ${watched ? "from" : "to"} watchlist`);
      });
    };
    rows.forEach(row => row.querySelector("[data-add]").addEventListener("click", () => {
      const symbol = row.dataset.symbol;
      list = list.includes(symbol) ? list.filter(item => item !== symbol) : [...list, symbol];
      saveList(list); render();
    }));
    search?.addEventListener("input", () => {
      const query = search.value.trim().toLowerCase(); let visible = 0;
      rows.forEach(row => { const match = row.dataset.search.toLowerCase().includes(query); row.hidden = !match; if (match) visible++; });
      empty.hidden = visible !== 0;
    });
    async function refreshSnapshot() {
      if (!board) return;
      try {
        const response = await fetch(board.dataset.snapshotUrl, { headers: { Accept: "application/json" }, cache: "no-store" });
        if (!response.ok) throw new Error("Snapshot request failed");
        const data = await response.json();
        data.assets.forEach(asset => {
          const row = document.querySelector(`tr[data-symbol="${asset.symbol}"]`);
          if (!row) return;
          row.querySelector(".market-price").textContent = new Intl.NumberFormat("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(asset.price);
          const change = row.querySelector(".change");
          change.textContent = `${asset.change >= 0 ? "+" : ""}${asset.change}%`;
          change.classList.toggle("up", asset.change >= 0); change.classList.toggle("down", asset.change < 0);
        });
        last.textContent = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
        source.textContent = data.live ? "Live crypto prices via market data feed" : "Latest available fallback prices";
      } catch (_) { source.textContent = "Live data temporarily unavailable"; }
    }
    render(); refreshSnapshot(); window.setInterval(refreshSnapshot, 60000);
  });
})();
