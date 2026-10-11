document.addEventListener("DOMContentLoaded", () => {
    initialiseFilterForm();
    initialiseMessages();
    initialiseDeleteConfirmations();
    initialiseMobileTableHint();
});


function initialiseFilterForm() {
    const filterForm = document.querySelector(".filters");

    if (!filterForm) {
        return;
    }

    const selectFilters = filterForm.querySelectorAll("select");

    selectFilters.forEach((select) => {
        select.addEventListener("change", () => {
            filterForm.submit();
        });
    });

    const searchInput = filterForm.querySelector('input[name="q"]');

    if (searchInput) {
        searchInput.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                searchInput.value = "";
                searchInput.focus();
            }
        });
    }
}


function initialiseMessages() {
    const messages = document.querySelectorAll(".messages .alert");

    console.log("Notifications found:", messages.length);

    messages.forEach(function (message) {
        setTimeout(function () {
            message.style.transition = "opacity 0.5s ease";
            message.style.opacity = "0";

            setTimeout(function () {
                message.remove();
            }, 500);
        }, 4000);
    });
}



function initialiseDeleteConfirmations() {
    const deleteForms = document.querySelectorAll(
        "[data-delete-confirm]"
    );

    deleteForms.forEach((form) => {
        form.addEventListener("submit", (event) => {
            const employeeName =
                form.dataset.employeeName || "this employee";

            const confirmed = window.confirm(
                `Delete ${employeeName}? This action cannot be undone.`
            );

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
}


function initialiseMobileTableHint() {
    const tables = document.querySelectorAll(".table-container");

    tables.forEach((tableContainer) => {
        if (tableContainer.scrollWidth > tableContainer.clientWidth) {
            tableContainer.setAttribute(
                "title",
                "Scroll horizontally to view the full table"
            );
        }
    });
}

function initialiseMobileMenu() {
    const button = document.getElementById("mobileMenuToggle");
    const sidebar = document.getElementById("sidebarNavigation");

    if (!button || !sidebar) return;

    button.addEventListener("click", () => {
        const isOpen = sidebar.classList.toggle("mobile-open");

        button.setAttribute("aria-expanded", String(isOpen));
        button.setAttribute(
            "aria-label",
            isOpen ? "Close navigation menu" : "Open navigation menu"
        );
    });
}

document.addEventListener("DOMContentLoaded", initialiseMobileMenu);


document.addEventListener("DOMContentLoaded", function () {
    const successMessages = document.querySelectorAll(
        '[data-message-tags~="success"]'
    );

    successMessages.forEach(function (message) {
        const text = message.textContent.trim();

        if (text.includes("has been deleted successfully.")) {
            alert(text);
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const notice = document.getElementById("employee-live-notice");

    if (!notice) return;

    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";

    const socket = new WebSocket(
        `${protocol}//${window.location.host}/ws/employees/`
    );

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);

        notice.textContent = data.message;
        notice.hidden = false;
    };

    socket.onerror = function () {
        console.warn("Employee notification connection failed.");
    };
});



document.addEventListener("DOMContentLoaded", function () {
    const notice = document.getElementById("employee-live-notice");

    if (!notice) return;

    const protocol =
        window.location.protocol === "https:" ? "wss:" : "ws:";

    const socket = new WebSocket(
        `${protocol}//${window.location.host}/ws/employees/`
    );

    socket.onopen = function () {
        console.log("WebSocket connected");
    };

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);

        console.log("Employee update received:", data.message);

        notice.textContent = data.message;
        notice.hidden = false;

        window.alert(data.message);
    };

    socket.onerror = function (error) {
        console.error("WebSocket connection failed:", error);
    };

    socket.onclose = function (event) {
        console.warn("WebSocket disconnected:", event.code);
    };
});
