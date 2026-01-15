// static/js/store.js

(function () {
  // Debounced search submit for the store search box
  const input = document.getElementById("productSearch");
  if (!input) return;

  const form = input.closest("form");
  if (!form) return;

  // Optional: live filter cards instantly as user types (nice UX)
  const cards = Array.from(document.querySelectorAll(".product-card"));

  let t = null;

  const liveFilter = (value) => {
    const q = value.trim().toLowerCase();
    if (!cards.length) return;

    cards.forEach((card) => {
      const title = (card.dataset.title || "").toLowerCase();
      const desc = (card.dataset.desc || "").toLowerCase();
      const match = !q || title.includes(q) || desc.includes(q);
      card.style.display = match ? "" : "none";
    });
  };

  input.addEventListener("input", function () {
    const value = input.value;

    // Live filter immediately
    liveFilter(value);

    // Debounce the real GET submit (keeps server-side search accurate too)
    if (t) clearTimeout(t);
    t = setTimeout(() => {
      // Only auto-submit if user typed something (or cleared)
      form.submit();
    }, 600);
  });

  // Enter key should submit immediately (normal behaviour)
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      if (t) clearTimeout(t);
      form.submit();
    }
  });
})();
