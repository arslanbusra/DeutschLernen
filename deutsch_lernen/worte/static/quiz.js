
const csrfToken = "{{ csrf_token }}";
let previousSelection = null; // Önceki seçimi tutmak için değişken

// Şıklar üzerine tıklama işlemleri
document.getElementById("list_app").addEventListener("click", function (event) {
    if (event.target.classList.contains("choice-btn")) {
        // Tüm şıklardan "selected" sınıfını kaldır
        document.querySelectorAll(".choice-btn").forEach(btn => btn.classList.remove("selected"));

        // Tıklanan butona "selected" sınıfını ekle
        event.target.classList.add("selected");

        // Önceki seçimi güncelle
        previousSelection = event.target.getAttribute("data-choice");

        console.log("Tıklanan buton:", event.target);
        console.log("Selected sınıfı eklendi mi?:", event.target.classList.contains("selected"));
    }
});

// Geri butonu
document.getElementById("but1").addEventListener("click", function () {
    fetch('/back/', {
        method: 'GET',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Yeni kelimeyi ekrana yazdır
            document.getElementById("par_app").textContent = `Wort: ${data.word}`;
            const listContainer = document.getElementById("list_app");
            listContainer.innerHTML = ""; // Şıkları temizle

            // Yeni şıkları ekle
            data.choiceswithlabels.forEach(choice => {
                const listItem = document.createElement("li");
                listItem.innerHTML = `<button class="choice-btn" data-choice="${choice[1]}">${choice[0]}: ${choice[1]}</button>`;
                listContainer.appendChild(listItem);
            });

            // Önceki seçimi geri yükle
            restorePreviousSelection();
        } else {
            console.error("Hata:", data.error);
        }
    })
    .catch(error => console.error('Fetch hatası:', error));
});

// İleri butonu
document.getElementById("but2").addEventListener("click", function () {
    fetch('/further/', {
        method: 'GET',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("par_app").textContent = `Wort: ${data.word}`;
            const listContainer = document.getElementById("list_app");
            listContainer.innerHTML = ""; // Şıkları temizle

            // Yeni şıkları ekle
            data.choiceswithlabels.forEach(choice => {
                const listItem = document.createElement("li");
                listItem.innerHTML = `<button class="choice-btn" data-choice="${choice[1]}">${choice[0]}: ${choice[1]}</button>`;
                listContainer.appendChild(listItem);
            });

            // Önceki seçimi geri yükle
            restorePreviousSelection();
        } else {
            console.error("Hata:", data.error);
        }
    })
    .catch(error => console.error('Fetch hatası:', error));
});

function restorePreviousSelection() {
    if (previousSelection) {
        const buttonToSelect = document.querySelector(`.choice-btn[data-choice="${previousSelection}"]`);
        if (buttonToSelect) {
            buttonToSelect.classList.add("selected");
            console.log("Önceki seçim geri yüklendi:", buttonToSelect);
        }
    }
}

// Sonuç butonu
document.getElementById("but3").addEventListener("click", function () {
    const selectedChoice = document.querySelector(".choice-btn.selected");

    if (!selectedChoice) {
        console.error("Hiçbir şık seçilmedi!");
        return;
    }

    console.log("Seçili buton:", selectedChoice);
    console.log("Seçili şık data-choice değeri:", selectedChoice.getAttribute("data-choice"));

    fetch('/result/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({ choice: selectedChoice.getAttribute("data-choice") }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Sonuç sayfasına yönlendirme
            window.location.href = '/result-page/';
        } else {
            console.error("Hata:", data.error);
        }
    })
    .catch(error => console.error('Fetch hatası:', error));
});



