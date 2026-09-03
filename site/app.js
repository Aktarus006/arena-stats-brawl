const $ = (selector) => document.querySelector(selector);
const esc = (value) => String(value).replace(/[&<>"]/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[char]));

function recordText(record) { return `${record.wins}–${record.losses}`; }
function rate(value) { return `${value.toFixed(1)}%`; }

function renderStats(target, values, empty = "No recorded flags") {
  const entries = Object.entries(values);
  target.innerHTML = entries.length ? `<div class="stat-list">${entries.map(([key, value]) => `<div class="stat"><span>${esc(key.replaceAll("_", " "))}</span><span>${esc(value)}</span></div>`).join("")}</div>` : `<p class="muted">${empty}</p>`;
}

function renderGames(games) {
  const target = $("#games");
  target.innerHTML = games.slice().reverse().map((game) => `<tr>
    <td>${String(game.id).padStart(3, "0")}</td>
    <td><span class="result ${game.result}">${game.result === "win" ? "WIN" : "LOSS"}</span></td>
    <td>${esc(game.opponent)}</td><td>${esc(game.archetype)}</td>
    <td><span class="pill">${esc(game.deck_version)}</span></td>
    <td class="${game.mana_issue === "none" ? "mana-ok" : "mana-flag"}">${esc(game.mana_issue.replaceAll("_", " "))}</td>
  </tr>`).join("");
}

async function init() {
  try {
    const response = await fetch("../data/dashboard.json");
    if (!response.ok) throw new Error(`Data request failed: ${response.status}`);
    const { games, summary } = await response.json();
    const overall = summary.overall;
    $("#overall-record").textContent = recordText(overall);
    $("#overall-rate").textContent = rate(overall.win_rate);
    const current = summary.versions["V2.1"] || overall;
    $("#experiment-record").textContent = `V2.1 — ${recordText(current)} (${rate(current.win_rate)})`;

    $("#versions").innerHTML = Object.entries(summary.versions).map(([name, stat]) => `<div class="version-row"><span class="version-label">${esc(name)}</span><div class="bar"><span style="width:${stat.win_rate}%"></span></div><small>${recordText(stat)} · ${rate(stat.win_rate)}</small></div>`).join("");
    const recent = summary.versions["V2.1"];
    const insight = recent && recent.games >= 10
      ? `V2.1 is ${recordText(recent)} across ${recent.games} games. Promising direction; keep the list stable until a larger block exists.`
      : "V2.1 needs a complete 10-game block before any conclusion.";
    const legacy = summary.versions["Legacy / unversioned"];
    $("#insights").innerHTML = `<div class="insight">${esc(insight)}</div><div class="insight warn">${legacy ? `${legacy.games} legacy games have no exact deck version. They remain useful history, not a controlled comparison.` : "Version data is complete."}</div><div class="insight">The dashboard reports records and exposure. It does not claim that a card caused a win without sufficient structured evidence.</div>`;
    renderStats($("#mana"), summary.mana_issues);
    renderStats($("#quality"), {"version captured": `${summary.data_quality.version_known}/${games.length}`, "archetype captured": `${summary.data_quality.archetype_known}/${games.length}`, "rank captured": `${summary.data_quality.rank_known}/${games.length}`});
    renderGames(games);
    $("#filter").addEventListener("input", (event) => {
      const needle = event.target.value.toLowerCase();
      renderGames(games.filter((game) => `${game.opponent} ${game.archetype} ${game.deck_version}`.toLowerCase().includes(needle)));
    });
  } catch (error) {
    document.querySelector(".shell").insertAdjacentHTML("afterbegin", `<div class="panel" role="alert"><strong>Dashboard data unavailable.</strong><p>Run <code>python3 tools/build_data.py</code>, then serve the repository root locally. ${esc(error.message)}</p></div>`);
  }
}
init();
