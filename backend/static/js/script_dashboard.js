async function carregarDadosDashboard() {
  const response = await fetch("/dados_dashboard");
  const payload = await response.json();

  if (!response.ok) {
    throw new Error(payload.error || "Falha ao obter dados do dashboard.");
  }

  return payload;
}

function criarGraficoPizza(categorias, valores) {
  const canvas = document.getElementById("graficoPizza");
  const contexto = canvas.getContext("2d");

  new Chart(contexto, {
    type: "pie",
    data: {
      labels: categorias,
      datasets: [
        {
          label: "Despesas por categoria",
          data: valores,
          backgroundColor: [
            "#ef4444",
            "#f59e0b",
            "#3b82f6",
            "#10b981",
            "#8b5cf6",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom",
        },
      },
    },
  });
}

async function inicializarDashboard() {
  const erroElement = document.getElementById("erroDashboard");
  erroElement.textContent = "";

  try {
    const dados = await carregarDadosDashboard();
    const despesas = dados.despesas_por_categoria || {};
    const categorias = Object.keys(despesas);
    const valores = Object.values(despesas);
    criarGraficoPizza(categorias, valores);
  } catch (error) {
    erroElement.textContent = `Erro: ${error.message}`;
  }
}

inicializarDashboard();
