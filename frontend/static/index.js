document.querySelector(".search-button").addEventListener("click", async () => {
  const input = document.querySelector(".search-box").value.trim();
  const recipeDiv = document.querySelector(".recipes");

  if (!input) {
    recipeDiv.innerHTML = `<p>Please enter an ingredient!</p>`;
    return;
  }

  recipeDiv.innerHTML = `<p>Loading recipes...</p>`;

  try {
    const response = await fetch("/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ingredient: input }),
    });

    const data = await response.json();

    if (data.error) {
      recipeDiv.innerHTML = `<p>${data.error}</p>`;
    } else {
      recipeDiv.innerHTML = `
        <h3>Recommended Recipes for "${input}"</h3>
        <div class="recipe-list">
          ${data.recipes
            .map(
              (r) => `
              <div class="recipe-card" onclick="window.location.href='/recipe/${encodeURIComponent(
                r.name
              )}'">
                <h4>${r.name}</h4>
                <p><b>Ingredients:</b> ${r.ingredients}</p>
              </div>
            `
            )
            .join("")}
        </div>
      `;
    }
  } catch (error) {
    recipeDiv.innerHTML = `<p>Something went wrong. Try again!</p>`;
    console.error(error);
  }
});
