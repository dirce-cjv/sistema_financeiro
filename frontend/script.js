const form = document.getElementById("import-form");
const fileInput = document.getElementById("excel-file");
const statusElement = document.getElementById("status");
const submitButton = document.getElementById("submit-button");

const API_URL = "http://localhost:3333/import/expenses";
const CATEGORIZE_URL = "http://localhost:3333/categorizar";

const categorizeButton = document.getElementById("categorize-button");
const categorizeStatus = document.getElementById("categorize-status");

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
  } catch (error) {
    categorizeStatus.textContent = `Erro: ${error.message}`;
  } finally {
    categorizeButton.disabled = false;
  }
});
