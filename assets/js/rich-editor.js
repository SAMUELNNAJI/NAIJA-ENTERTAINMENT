/* Lightweight Summernote-style editor for post bodies; stores HTML in the form textarea. */
(function () {
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-rich-editor]").forEach(function (editor) {
      var source = editor.querySelector("textarea");
      var surface = editor.querySelector("[data-rich-surface]");
      if (!source || !surface) return;
      surface.innerHTML = source.value;
      source.hidden = true;
      source.setAttribute("aria-hidden", "true");
      function sync() { source.value = surface.innerHTML.trim(); }
      surface.addEventListener("input", sync);
      editor.querySelector(".rich-editor__toolbar").addEventListener("click", function (event) {
        var button = event.target.closest("button[data-command]");
        if (!button) return;
        event.preventDefault();
        surface.focus();
        var command = button.dataset.command;
        if (command === "createLink") {
          var url = window.prompt("Paste a link (https://…)");
          if (!url) return;
          document.execCommand("createLink", false, url);
        } else document.execCommand(command, false, button.dataset.value || null);
        sync();
      });
      source.form.addEventListener("submit", sync);
    });
  });
})();
