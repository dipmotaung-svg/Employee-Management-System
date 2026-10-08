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
    const messages = document.querySelectorAll(".message");

    messages.forEach((message) => {
        window.setTimeout(() => {
            message.classList.add("is-hiding");

            window.setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
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