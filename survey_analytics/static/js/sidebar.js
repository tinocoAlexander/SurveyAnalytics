function toggleMenu() {
    const sidebar = document.getElementById("sidebar");
    if (sidebar.style.left === "0px") {
        sidebar.style.left = "-100%";
    } else {
        sidebar.style.left = "0px";
    }
}
