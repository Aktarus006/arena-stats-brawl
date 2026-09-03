const $ = (selector) => document.querySelector(selector);
const esc = (value) => String(value).replace(/[&<>"']/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#039;"}[char]));
let dashboard;

function recordText(record) { return `${record.wins}–${record.losses}`; }
function rate(value) { return `${value.toFixed(1)}%`; }
function renderStats(target, values, empty = "Aucun flag enregistré") {
  const entries = Object.entries(values);
  target.innerHTML = entries.length ? `<div class="stat-list">${entries.map(([key, value]) => `<div class="stat"><span>${esc(key.replaceAll("_", " "))}</span><b>${esc(value)}</b></div>`).join("")}</div>` : `<p>${empty}</p>`;
}
function renderGames(games) {
  $("#games").innerHTML = games.slice().reverse().map((game) => `<tr><td>${String(game.id).padStart(3, "0")}</td><td><span class="result ${game.result}">${game.result === "win" ? "WIN" : "LOSS"}</span></td><td>${esc(game.opponent)}</td><td>${esc(game.archetype)}</td><td>${esc(game.deck_version)}</td><td>${esc(game.mana_issue.replaceAll("_", " "))}</td></tr>`).join("");
}
function renderDeck(cards) {
  $("#deck-cards").innerHTML = cards.map((card) => `<div class="deck-card"><b>${card.quantity}×</b><span>${esc(card.name)}</span></div>`).join("");
}
function render(data) {
  dashboard = data;
  const { games, summary, deck } = data;
  $("#overall-record").textContent = recordText(summary.overall);
  $("#overall-rate").textContent = rate(summary.overall.win_rate);
  const current = summary.versions.V2_1 || summary.versions["V2.1"] || summary.overall;
  $("#experiment-record").textContent = `${recordText(current)} · ${rate(current.win_rate)}`;
  $("#next-game").textContent = String(Math.max(...games.map((game) => game.id)) + 1).padStart(3, "0");
  $("#versions").innerHTML = Object.entries(summary.versions).map(([name, stat]) => `<div class="version-row"><b>${esc(name)}</b><div class="bar"><i style="width:${stat.win_rate}%"></i></div><span>${recordText(stat)} / ${rate(stat.win_rate)}</span></div>`).join("");
  const v21 = summary.versions["V2.1"];
  $("#insights").innerHTML = `<p><b>V2.1 :</b> ${v21 ? `${recordText(v21)} sur ${v21.games} games.` : "en attente de données."}</p><p>Le site conserve les données structurées ; une carte n’est jamais déclarée décisive sans exposition suffisante.</p><p>La liste est stable jusqu’à G80, sauf signal manifeste.</p>`;
  renderStats($("#mana"), summary.mana_issues);
  renderStats($("#quality"), {"version": `${summary.data_quality.version_known}/${games.length}`, "archétype": `${summary.data_quality.archetype_known}/${games.length}`, "rank": `${summary.data_quality.rank_known}/${games.length}`});
  $("#commander-name").textContent = deck.list.commander;
  $("#deck-total").textContent = deck.list.total_cards;
  renderGames(games);
  renderDeck(deck.list.cards);
  $("#filter").oninput = (event) => { const q = event.target.value.toLowerCase(); renderGames(games.filter((game) => `${game.opponent} ${game.archetype} ${game.deck_version}`.toLowerCase().includes(q))); };
  $("#deck-filter").oninput = (event) => { const q = event.target.value.toLowerCase(); renderDeck(deck.list.cards.filter((card) => card.name.toLowerCase().includes(q))); };
}
async function refresh() {
  const response = await fetch("../data/dashboard.json", { cache: "no-store" });
  if (!response.ok) throw new Error(`Impossible de charger les données (${response.status}).`);
  render(await response.json());
}
function setupForm() {
  $("#game-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const status = $("#form-status");
    const submit = form.querySelector("button[type=submit]");
    const payload = Object.fromEntries(new FormData(form));
    payload.mvp = payload.mvp.split(",").map((card) => card.trim()).filter(Boolean);
    submit.disabled = true; status.textContent = "ENREGISTREMENT…";
    try {
      const response = await fetch("/api/games", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Enregistrement impossible.");
      status.textContent = `GAME ${String(data.game.id).padStart(3, "0")} ENREGISTRÉE. DASHBOARD RÉGÉNÉRÉ.`;
      form.reset(); form.elements.rank.value = "Gold 3"; form.elements.mulligans.value = "0";
      await refresh();
    } catch (error) { status.textContent = `ERREUR : ${error.message}`; }
    finally { submit.disabled = false; }
  });
}
refresh().then(setupForm).catch((error) => { document.body.insertAdjacentHTML("afterbegin", `<p class="fatal">${esc(error.message)} Lancez <code>python3 tools/serve.py</code>.</p>`); });
