document.addEventListener("DOMContentLoaded", function () {
  // Suppression d'un article
  document.querySelectorAll(".product .fa-trash-can").forEach((button) => {
    button.addEventListener("click", function () {
      const productId = this.closest(".product").dataset.productId;
      fetch(`/cart/remove/${productId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCSRFToken(),
          "Content-Type": "application/json",
        },
      }).then((response) => {
        if (response.ok) {
          location.reload(); // Recharger la page pour mettre à jour le panier
        }
      });
    });
  });

  // Augmenter la quantité
  document.querySelectorAll(".product .increase").forEach((button) => {
    button.addEventListener("click", function () {
      const productId = this.closest(".product").dataset.productId;
      updateQuantity(productId, 1); // Ajouter 1
    });
  });

  // Diminuer la quantité
  document.querySelectorAll(".product .decrease").forEach((button) => {
    button.addEventListener("click", function () {
      const productId = this.closest(".product").dataset.productId;
      updateQuantity(productId, -1); // Soustraire 1
    });
  });

  // Vider le panier
  document.querySelector(".clear").addEventListener("click", function () {
    fetch("/cart/clear/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
        "Content-Type": "application/json",
      },
    }).then((response) => {
      if (response.ok) {
        location.reload();
      }
    });
  });

  // Fonction pour mettre à jour la quantité
  function updateQuantity(productId, delta) {
    fetch(`/cart/update/${productId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ delta: delta }),
    }).then((response) => {
      if (response.ok) {
        location.reload(); // Recharger la page pour voir la quantité mise à jour
      }
    });
  }

  // Fonction pour obtenir le token CSRF
  function getCSRFToken() {
    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;
    return csrfToken;
  }
});
