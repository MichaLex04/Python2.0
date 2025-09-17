// main.js

document.addEventListener("DOMContentLoaded", () => {
  const recetaSelect = document.getElementById("recetaSelect");
  const personasInput = document.getElementById("personasInput");
  const racionForm = document.getElementById("racionForm");
  const ingredientesTableBody = document.querySelector("#ingredientesTable tbody");
  const precioTotalSpan = document.getElementById("precioTotal");

  const promptAI = document.getElementById("promptAI");
  const generarRecetaBtn = document.getElementById("generarRecetaBtn");
  const recetaGeneradaDiv = document.getElementById("recetaGenerada");
  const guardarRecetaBtn = document.getElementById("guardarRecetaBtn");

  // Cargar recetas desde backend (simulado con fetch)
  async function cargarRecetas() {
    try {
      const res = await fetch("/api/recetas");
      const data = await res.json();
      recetaSelect.innerHTML = "";
      data.forEach((receta) => {
        const option = document.createElement("option");
        option.value = receta.id;
        option.textContent = receta.nombre;
        recetaSelect.appendChild(option);
      });
    } catch (error) {
      alert("Error cargando recetas");
      console.error(error);
    }
  }

  // Calcular ingredientes ajustados
  async function calcularRacion(recetaId, personas) {
    try {
      const res = await fetch(`/api/calcular?receta_id=${recetaId}&personas=${personas}`);
      const data = await res.json();

      ingredientesTableBody.innerHTML = "";
      let totalPrecio = 0;

      data.ingredientes.forEach((ing) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${ing.nombre}</td>
          <td>${ing.cantidad_ajustada}</td>
          <td>${ing.precio_por_racion.toFixed(2)}</td>
        `;
        ingredientesTableBody.appendChild(tr);
        totalPrecio += ing.precio_por_racion;
      });

      precioTotalSpan.textContent = totalPrecio.toFixed(2);
    } catch (error) {
      alert("Error calculando ración");
      console.error(error);
    }
  }

  racionForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const recetaId = recetaSelect.value;
    const personas = parseInt(personasInput.value);
    if (recetaId && personas > 0) {
      calcularRacion(recetaId, personas);
    }
  });

  // Generar receta con IA
  generarRecetaBtn.addEventListener("click", async () => {
    const prompt = promptAI.value.trim();
    if (!prompt) {
      alert("Por favor, escribe una descripción para generar la receta.");
      return;
    }
    recetaGeneradaDiv.textContent = "Generando receta...";
    guardarRecetaBtn.style.display = "none";

    try {
      const res = await fetch("/api/generar_receta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      recetaGeneradaDiv.textContent = data.receta_texto;
      guardarRecetaBtn.style.display = "inline-block";
    } catch (error) {
      recetaGeneradaDiv.textContent = "Error generando receta.";
      console.error(error);
    }
  });

  // Guardar receta generada
  guardarRecetaBtn.addEventListener("click", async () => {
    const recetaTexto = recetaGeneradaDiv.textContent;
    if (!recetaTexto) return;

    try {
      const res = await fetch("/api/guardar_receta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ receta_texto: recetaTexto }),
      });
      const data = await res.json();
      if (data.success) {
        alert("Receta guardada correctamente.");
        guardarRecetaBtn.style.display = "none";
        recetaGeneradaDiv.textContent = "";
        promptAI.value = "";
        cargarRecetas();
      } else {
        alert("Error guardando receta.");
      }
    } catch (error) {
      alert("Error guardando receta.");
      console.error(error);
    }
  });

  // Inicializar
  cargarRecetas();
});