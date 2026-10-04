// Tag Markdown tables whose first header is "No." so CSS can size their columns.
// A data attribute (not a class) keeps Material's `table:not([class])` styling.
function tagNumberedTables() {
  document.querySelectorAll(".md-typeset table").forEach(function (table) {
    var first = table.querySelector("thead th");
    if (first && first.textContent.trim().replace(/\.$/, "").toLowerCase() === "no") {
      table.setAttribute("data-numbered", "");
    }
  });
}

if (typeof document$ !== "undefined") {
  document$.subscribe(tagNumberedTables);
} else {
  document.addEventListener("DOMContentLoaded", tagNumberedTables);
}
