function showSection(id) {
  document.querySelectorAll('.section').forEach(sec => sec.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

function login() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;

  fetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        window.loggedInUser = username;
        alert("Login successful!");
        showMenuPage();
        document.getElementById("scrollContainer").style.display = "block"; // reset visibility
      } else {
        alert("Login failed: " + data.message);
      }
    })
    .catch(err => {
      console.error(err);
      alert("Server error. Try again.");
    });
}

function signup() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;

  if (!username || !password) {
    alert("Please fill out both username and password fields.");
    return;
  }

  fetch('/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        window.loggedInUser = username;
        alert("Signup successful!");
        showMenuPage();
        document.getElementById("scrollContainer").style.display = "block"; // reset visibility
      } else {
        alert("Signup failed: " + data.message);
      }
    })
    .catch(err => {
      console.error(err);
      alert("Server error. Try again.");
    });
}

function finish() {
  showSection('finalSection');
}

function restart() {
  showSection('authSection');
  // document.getElementById("scrollContainer").style.display = "block"; // reset visibility
}

// =================== MENU PAGE ===================

function showMenuPage() {
  showSection('foodSection');
  const menuTable = document.querySelector("#menuTable tbody");
  const recTable = document.querySelector("#recTable tbody");
  menuTable.innerHTML = "";
  recTable.innerHTML = "";

  fetch('/get_menu')
    .then(res => res.json())
    .then(allItems => {
      fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: window.loggedInUser })
      })
        .then(res => res.json())
        .then(recommendedItems => {
          const recommendedNames = recommendedItems.map(item => item.name);
          window.recommendedData = recommendedItems;
          window.menuData = allItems.filter(item => !recommendedNames.includes(item.name));

          // Show recommended table if available
          if (recommendedItems.length > 0) {
            document.getElementById("recSection").style.display = "block";
            recommendedItems.forEach((item, index) => {
              const row = document.createElement("tr");
              row.innerHTML = `
                <td>${item.name}</td>
                <td>${item.price}</td>
                <td>
                  <input type="number" id="rec-item-${index}" min="0" max="10" value="0">
                </td>
              `;
              recTable.appendChild(row);
            });
          } else {
            document.getElementById("recSection").style.display = "none";
          }

          // Add remaining menu items
          window.menuData.forEach((item, index) => {
            const row = document.createElement("tr");
            row.innerHTML = `
              <td>${item.name}</td>
              <td>${item.price}</td>
              <td>
                <input type="number" id="item-${index}" min="0" max="10" value="0">
              </td>
            `;
            menuTable.appendChild(row);
          });
        });
    });
}

function showBill() {
  document.getElementById("scrollContainer").style.display = "none";
  showSection("billSection");

  const billTable = document.getElementById("billTable").getElementsByTagName("tbody")[0];
  billTable.innerHTML = "";
  let total = 0;

  // Recommended items
  if (window.recommendedData) {
    window.recommendedData.forEach((item, index) => {
      const qty = parseInt(document.getElementById(`rec-item-${index}`).value) || 0;
      if (qty > 0) {
        const itemTotal = item.price * qty;
        total += itemTotal;

        const newRow = billTable.insertRow();
        newRow.insertCell(0).innerText = item.name;
        newRow.insertCell(1).innerText = item.price;
        newRow.insertCell(2).innerText = qty;
        newRow.insertCell(3).innerText = itemTotal;
      }
    });
  }

  // Normal menu items
  if (window.menuData) {
    window.menuData.forEach((item, index) => {
      const qty = parseInt(document.getElementById(`item-${index}`).value) || 0;
      if (qty > 0) {
        const itemTotal = item.price * qty;
        total += itemTotal;

        const newRow = billTable.insertRow();
        newRow.insertCell(0).innerText = item.name;
        newRow.insertCell(1).innerText = item.price;
        newRow.insertCell(2).innerText = qty;
        newRow.insertCell(3).innerText = itemTotal;
      }
    });
  }

  document.getElementById("grandTotal").innerText = `Total: ₹${total}`;
}

function goToCheckout() {
  // Could send order to backend if needed
  finish();
}

function goBack() {
  showSection("foodSection");
  document.getElementById("scrollContainer").style.display = "block";
}
