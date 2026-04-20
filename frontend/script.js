const form = document.getElementById("import-form");
const fileInput = document.getElementById("excel-file");
const statusElement = document.getElementById("status");
const submitButton = document.getElementById("submit-button");

const API_URL = "http://localhost:3333/import/expenses";
const CATEGORIZE_URL = "http://localhost:3333/categorizar";
const DASHBOARD_DATA_URL = "http://localhost:3333/dados_dashboard";

const categorizeButton = document.getElementById("categorize-button");
const categorizeStatus = document.getElementById("categorize-status");
const refreshDashboardButton = document.getElementById("refresh-dashboard-button");
const dashboardStatus = document.getElementById("dashboard-status");

let pizzaChart = null;

function formatCurrencyBRL(value) {
  return Number(value || 0).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
}

function renderDashboardChart(despesasPorCategoria) {
  const categorias = Object.keys(despesasPorCategoria || {});
  const valores = Object.values(despesasPorCategoria || {});
  const canvas = document.getElementById("graficoPizza");
  const ctx = canvas.getContext("2d");

  if (pizzaChart) {
    pizzaChart.destroy();
  }

  pizzaChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: categorias,
      datasets: [
        {
          data: valores,
          backgroundColor: ["#ef4444", "#f59e0b", "#3b82f6", "#10b981", "#8b5cf6"],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "bottom" },
        tooltip: {
          callbacks: {
            label(context) {
              const label = context.label || "";
              const raw = context.raw || 0;
              return `${label}: ${formatCurrencyBRL(raw)}`;
            },
          },
        },
      },
    },
  });
}

async function loadDashboardData() {
  refreshDashboardButton.disabled = true;
  dashboardStatus.textContent = "Carregando dashboard...";

  try {
    const response = await fetch(DASHBOARD_DATA_URL);
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.error || "Falha ao carregar dashboard.");
    }

    const despesas = payload.despesas_por_categoria || {};
    renderDashboardChart(despesas);

    const total = Object.values(despesas).reduce((acc, value) => acc + Number(value || 0), 0);
    dashboardStatus.textContent = `Dashboard atualizado. Total de despesas: ${formatCurrencyBRL(total)}.`;
  } catch (error) {
    dashboardStatus.textContent = `Erro: ${error.message}`;
  } finally {
    refreshDashboardButton.disabled = false;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!fileInput.files || fileInput.files.length === 0) {
    statusElement.textContent = "Selecione um arquivo para importar.";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  submitButton.disabled = true;
  statusElement.textContent = "Importando arquivo...";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      body: formData,
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.error || "Falha na importacao.");
    }

    statusElement.textContent =
      "Importacao finalizada com sucesso.\n" +
      `Linhas importadas: ${payload.imported_rows}\n` +
      `IDs gerados: ${payload.start_id} ate ${payload.end_id}`;
    await loadDashboardData();
  } catch (error) {
    statusElement.textContent = `Erro: ${error.message}`;
  } finally {
    submitButton.disabled = false;
  }
});

categorizeButton.addEventListener("click", async () => {
  categorizeButton.disabled = true;
  categorizeStatus.textContent = "Categorizando...";

  try {
    const response = await fetch(CATEGORIZE_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: "{}",
    });

    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.error || "Falha na categorizacao.");
    }

    if (payload.processed === 0) {
      categorizeStatus.textContent = payload.message || "Nenhuma linha para categorizar.";
      return;
    }

    const preview = payload.rows
      .slice(0, 8)
      .map((r) => `ID ${r.id}: ${r.categoria}`)
      .join("\n");
    const more =
      payload.rows.length > 8
        ? `\n... e mais ${payload.rows.length - 8} linha(s).`
        : "";

    categorizeStatus.textContent =
      `${payload.message}\n` +
      `Linhas processadas: ${payload.processed}\n\n` +
      preview +
      more;
    await loadDashboardData();
  } catch (error) {
    categorizeStatus.textContent = `Erro: ${error.message}`;
  } finally {
    categorizeButton.disabled = false;
  }
});

refreshDashboardButton.addEventListener("click", async () => {
  await loadDashboardData();
});

loadDashboardData();
