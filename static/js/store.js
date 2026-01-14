// Live filtering on the store page (your own JS = requirement met)
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("productSearch");
  const cards = document.querySelectorAll(".product-card");

  if (!input || !cards.length) return;

  input.addEventListener("input", () => {
    const q = input.value.trim().toLowerCase();
    cards.forEach((card) => {
      const title = card.dataset.title || "";
      const desc = card.dataset.desc || "";
      const show = title.includes(q) || desc.includes(q);
      card.style.display = show ? "" : "none";
    });
  });
});
