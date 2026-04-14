const form = document.getElementById("uploadForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(form);

  const res = await fetch("http://localhost:5000/api/invoice/upload", {
    method: "POST",
    body: formData
  });

  const data = await res.json();

  document.getElementById("result").innerText = JSON.stringify(data, null, 2);
});
