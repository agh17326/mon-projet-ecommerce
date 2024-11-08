document.addEventListener("DOMContentLoaded", function () {
  const addToCartButton = document.querySelector(".add-to-cart");

  if (addToCartButton) {
    addToCartButton.addEventListener("click", function (event) {
      event.preventDefault();
      const productId = window.location.pathname
        .split("/")
        .filter(Boolean)
        .pop(); // Récupère l'ID du produit depuis l'URL

      fetch(`/ajouter_au_panier/${productId}/`, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.message) {
            alert(data.message);
            // Met à jour la quantité affichée dans le panier ou autre indication visuelle
          }
        })
        .catch((error) => console.error("Erreur:", error));
    });
  }
});
