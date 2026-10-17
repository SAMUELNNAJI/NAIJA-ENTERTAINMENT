/* AJAX comments: create, edit, delete and one-level replies. */
(function () {
  function csrf() { var match = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/); return match ? decodeURIComponent(match[1]) : ""; }
  function post(url, data) {
    return fetch(url, {method:"POST", headers:{"X-Requested-With":"XMLHttpRequest","X-CSRFToken":csrf(),"Content-Type":"application/x-www-form-urlencoded"}, body:new URLSearchParams(data)})
      .then(async function (response) { var json = await response.json(); if (!response.ok) throw json; return json; });
  }
  function error(err) { alert((err && (err.error || (err.errors && Object.values(err.errors).flat().join("\n")))) || "Network error — try again."); }
  function updateCount() { var thread = document.getElementById("comment-thread"), count = document.querySelector("[data-comment-count]"); if (!thread || !count) return; var total = thread.querySelectorAll(".comment-sticker").length; count.textContent = total + " comment" + (total === 1 ? "" : "s"); }
  function closeEditor(sticker) { if (!sticker) return; var text = sticker.querySelector(".body-text"), form = sticker.querySelector(".comment-edit-form"); if (text) text.style.display = ""; if (form) form.style.display = "none"; }

  document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function (event) {
      var edit = event.target.closest("[data-edit-comment]");
      if (edit) { event.preventDefault(); var sticker = document.getElementById("comment-" + edit.dataset.editComment); if (sticker) { sticker.querySelector(".body-text").style.display = "none"; sticker.querySelector(".comment-edit-form").style.display = "block"; } return; }
      var cancel = event.target.closest("[data-cancel-edit]");
      if (cancel) { closeEditor(document.getElementById("comment-" + cancel.dataset.cancelEdit)); return; }
      var remove = event.target.closest("[data-delete-comment]");
      if (remove) { if (!confirm("Delete this comment and its replies?")) return; post("/comment/" + remove.dataset.deleteComment + "/delete/", {}).then(function () { var node = document.getElementById("comment-" + remove.dataset.deleteComment); var wrap = node && node.closest(".reply-wrap"); if (wrap) wrap.remove(); else if (node) { var next = node.nextElementSibling; while (next && next.classList.contains("reply-wrap")) { var following = next.nextElementSibling; next.remove(); next = following; } node.remove(); } var thread = document.getElementById("comment-thread"); if (thread && !thread.querySelector(".comment-sticker")) thread.innerHTML = '<p class="mad-no-comments">No thoughts here yet. Be the spark.</p>'; updateCount(); }).catch(error); return; }
      var reply = event.target.closest("[data-reply-comment]");
      if (reply) { var slot = document.querySelector("[data-reply-slot='" + reply.dataset.replyComment + "']"); if (!slot || slot.innerHTML) return; var slug = document.getElementById("comment-thread").dataset.slug; slot.innerHTML = '<form class="form-fab comment-reply-form" action="/blog/' + slug + '/comment/"><textarea name="body" required placeholder="Write a reply…"></textarea><input type="hidden" name="parent" value="' + reply.dataset.replyComment + '"><div class="edit-controls"><button class="mad-btn sm" type="submit">Reply</button><button class="mad-btn sm ghost" type="button" data-cancel-reply>Cancel</button></div></form>'; slot.querySelector("textarea").focus(); return; }
      var cancelReply = event.target.closest("[data-cancel-reply]"); if (cancelReply) cancelReply.closest(".comment-reply-slot").innerHTML = "";
    });
    document.addEventListener("submit", function (event) {
      var form = event.target.closest("form[data-comment-form], form.comment-reply-form, form.comment-edit-form");
      if (!form) return;
      event.preventDefault(); var data = Object.fromEntries(new FormData(form)); var button = form.querySelector("button[type='submit']"); if (button) button.disabled = true;
      post(form.action, data).then(function (res) {
        if (form.classList.contains("comment-edit-form")) { var sticker = form.closest(".comment-sticker"), text = sticker.querySelector(".body-text"); text.textContent = res.comment.body; closeEditor(sticker); return; }
        var thread = document.getElementById("comment-thread"); var empty = thread.querySelector(".mad-no-comments"); if (empty) empty.remove();
        if (form.classList.contains("comment-reply-form")) { var parent = document.getElementById("comment-" + data.parent); var wrap = document.createElement("div"); wrap.className = "reply-wrap"; wrap.innerHTML = res.comment_html; var old = parent.parentNode.querySelector(":scope > .reply-wrap:last-child"); if (old) old.after(wrap); else parent.after(wrap); form.closest(".comment-reply-slot").innerHTML = ""; }
        else { thread.insertAdjacentHTML("afterbegin", res.comment_html); form.querySelector("textarea").value = ""; }
        updateCount();
      }).catch(error).finally(function () { if (button) button.disabled = false; });
    });
  });
})();
