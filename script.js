document.addEventListener("DOMContentLoaded", function () {
    // Read More Toggle
    const buttons = document.querySelectorAll(".read-more");
    buttons.forEach(button => {
        button.addEventListener("click", function () {
            const extraContent = this.previousElementSibling;
            if (extraContent.style.display === "none" || extraContent.style.display === "") {
                extraContent.style.display = "block";
                this.textContent = "Read Less";
            } else {
                extraContent.style.display = "none";
                this.textContent = "Read More";
            }
        });
    });

    // Like Button Functionality
    const likeButtons = document.querySelectorAll(".like-btn");
    likeButtons.forEach(button => {
        button.addEventListener("click", function () {
            const likeCount = this.querySelector(".like-count");
            likeCount.textContent = parseInt(likeCount.textContent) + 1;
        });
    });

    // Reaction Button Functionality
    const reactionButtons = document.querySelectorAll(".reaction");
    reactionButtons.forEach(button => {
        button.addEventListener("click", function () {
            const countSpan = this.querySelector(".reaction-count");
            countSpan.textContent = parseInt(countSpan.textContent) + 1;
        });
    });

    // Search Functionality
    const searchInput = document.getElementById("search-input");
    searchInput.addEventListener("input", function () {
        const filter = searchInput.value.toLowerCase();
        const blogCards = document.querySelectorAll(".blog-card");
        blogCards.forEach(card => {
            const title = card.getAttribute("data-title").toLowerCase();
            if (title.includes(filter)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    });
});
