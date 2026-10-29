async function updateScreenshot(row) {
    try {
        const response = await fetch(row.dataset.statusUrl, {
            cache: "no-store",
        });
        if (!response.ok) {
            throw new Error("Could not check screenshot status");
        }

        const data = await response.json();
        const badge = row.querySelector("[data-status]");
        const placeholder = row.querySelector("[data-file-placeholder]");
        row.dataset.state = data.status;
        badge.textContent = data.label;
        badge.classList.remove(
            "text-bg-warning", "text-bg-success", "text-bg-danger",
        );
        badge.classList.add({
            PE: "text-bg-warning",
            SU: "text-bg-success",
            FA: "text-bg-danger",
        }[data.status]);

        if (data.status === "SU" && data.file_url) {
            const link = row.querySelector("[data-file-link]");
            link.href = data.file_url;
            link.hidden = false;
            placeholder.hidden = true;
            return;
        }

        if (data.status === "FA") {
            placeholder.textContent = "Capture failed.";
            return;
        }

        placeholder.textContent = "Capturing...";
    } catch (error) {
        const placeholder = row.querySelector("[data-file-placeholder]");
        placeholder.textContent = "Reconnecting...";
    }

    setTimeout(() => updateScreenshot(row), 2000);
}

document.querySelectorAll('tr[data-state="PE"]').forEach((row) => {
    setTimeout(() => updateScreenshot(row), 1000);
});
