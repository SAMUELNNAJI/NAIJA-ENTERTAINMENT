/* Currency conversion stays entirely on the page; fresh rates arrive in the background. */
(function () {
  "use strict";
  const KEY = "tne-converter-2";

  document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#form");
    if (!form) return;
    const amount = document.querySelector("#amount");
    const from = document.querySelector("#from");
    const to = document.querySelector("#to");
    const result = document.querySelector("#result");
    const detail = document.querySelector("#rate-detail");
    const status = document.querySelector("#rate-status");
    const chips = document.querySelector("#chips");
    const initial = document.querySelector("#rates-json");
    let rates = initial ? JSON.parse(initial.textContent || "{}") : {};

    try {
      amount.value = localStorage.getItem(KEY + ":amount") || amount.value;
      from.value = localStorage.getItem(KEY + ":from") || "USD";
      to.value = localStorage.getItem(KEY + ":to") || "NGN";
    } catch (_) {}

    const number = (value, digits, fixed = false) => new Intl.NumberFormat("en-NG", { maximumFractionDigits: digits, minimumFractionDigits: fixed ? digits : 0 }).format(value);
    const persist = () => { try { localStorage.setItem(KEY + ":amount", amount.value); localStorage.setItem(KEY + ":from", from.value); localStorage.setItem(KEY + ":to", to.value); } catch (_) {} };
    function convert() {
      const input = Math.max(0, Number(amount.value) || 0);
      // Rates are normalised as "how many NGN one unit buys". Convert via NGN:
      // source amount × source NGN value ÷ destination NGN value.
      const rate = rates[from.value] && rates[to.value] ? rates[from.value] / rates[to.value] : 0;
      const output = input * rate;
      result.innerHTML = `<span class="result-label">${number(input, 2, true)} ${from.value} equals</span><strong>${rate ? number(output, 2, true) : "—"} <small>${to.value}</small></strong>`;
      detail.textContent = rate ? `1 ${from.value} = ${number(rate, 6)} ${to.value}` : "This pair is not available right now.";
    }
    function renderChips() {
      const popular = ["NGN", "USD", "GBP", "EUR", "GHS", "AED"];
      chips.replaceChildren(...popular.filter(code => rates[code]).map(code => {
        const button = document.createElement("button");
        button.type = "button"; button.textContent = code;
        button.addEventListener("click", () => { to.value = code; convert(); persist(); });
        return button;
      }));
    }
    function setStatus(live) {
      status.textContent = live ? "Live rate" : "Latest available rate";
      status.classList.toggle("is-live", live);
    }
    async function refresh() {
      try {
        const response = await fetch(form.dataset.ratesUrl, { headers: { Accept: "application/json" }, cache: "no-store" });
        if (!response.ok) throw new Error("Rate request failed");
        const data = await response.json();
        rates = data.rates || rates; setStatus(Boolean(data.live)); renderChips(); convert();
      } catch (_) { setStatus(false); convert(); }
    }
    form.addEventListener("submit", event => { event.preventDefault(); convert(); persist(); });
    amount.addEventListener("input", () => { convert(); persist(); });
    document.querySelectorAll("[data-amount]").forEach(button => button.addEventListener("click", () => { amount.value = button.dataset.amount; convert(); persist(); }));
    [from, to].forEach(select => select.addEventListener("change", () => { convert(); persist(); }));
    document.querySelector("#swap").addEventListener("click", () => { [from.value, to.value] = [to.value, from.value]; convert(); persist(); });
    renderChips(); convert(); refresh(); window.setInterval(refresh, 60000);
  });
})();
