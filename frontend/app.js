document.addEventListener("DOMContentLoaded", () => {
  const select_pref = document.getElementById("prefSelect");

  fetch("http://localhost:8000/prefectures")  // バックエンドAPI
    .then(res => res.json())
    .then(data => {
      data.forEach(pref => {
        const opt = document.createElement("option");
        opt.value = pref.code;         // 例: "13"
        opt.textContent = pref.name;   // 例: "東京都"
        select_pref.appendChild(opt);
      });
    })
    .catch(err => {
      console.error("都道府県の取得に失敗しました:", err);
    });
});
