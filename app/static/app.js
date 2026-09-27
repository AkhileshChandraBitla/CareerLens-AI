const resume = document.getElementById("resume");
const fileName = document.getElementById("fileName");
const status = document.getElementById("status");
const results = document.getElementById("results");

resume.addEventListener("change", () => {
  fileName.textContent = resume.files[0]?.name || "Choose PDF or DOCX";
});

function renderChips(id, values) {
  const el = document.getElementById(id);
  el.innerHTML = values.length
    ? values.map(v => `<span class="chip">${v}</span>`).join("")
    : `<span class="chip">None detected</span>`;
}

document.getElementById("analyze").addEventListener("click", async () => {
  const job = document.getElementById("job").value.trim();
  if (!resume.files[0] || !job) {
    status.textContent = "Please upload a resume and paste a job description.";
    return;
  }
  const form = new FormData();
  form.append("resume", resume.files[0]);
  form.append("job_description", job);
  status.textContent = "Analyzing resume…";
  results.classList.add("hidden");

  try {
    const response = await fetch("/api/analyze", {method:"POST", body:form});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Analysis failed");
    document.getElementById("score").textContent = data.score + "%";
    document.getElementById("semantic").textContent = data.semantic_similarity + "%";
    document.getElementById("coverage").textContent = data.skill_coverage + "%";
    renderChips("matched", data.matched_skills);
    renderChips("missing", data.missing_skills);
    document.getElementById("suggestions").innerHTML =
      data.suggestions.map(s => `<li>${s}</li>`).join("");
    results.classList.remove("hidden");
    status.textContent = `Analysis complete for ${data.resume_name}.`;
  } catch (e) {
    status.textContent = e.message;
  }
});
