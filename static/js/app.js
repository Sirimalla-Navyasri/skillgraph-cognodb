async function loadSimilarCandidates(candidateId) {

    const container =
        document.getElementById("similar-results");

    container.innerHTML =
        "<p>Finding similar candidates...</p>";

    try {

        const response =
            await fetch(
                `/api/candidate/${candidateId}/similar`
            );

        const data =
            await response.json();

        if (!data.success) {

            container.innerHTML =
                "<p>Unable to load recommendations.</p>";

            return;
        }

        if (data.results.length === 0) {

            container.innerHTML =
                "<p>No similar candidates found.</p>";

            return;
        }

        container.innerHTML =
            data.results.map(candidate => `
                <div class="card">
                    <h3>${candidate.name}</h3>
                    <p>${candidate.title}</p>
                    <p>
                        Shared skills:
                        ${candidate.shared_skills}
                    </p>
                </div>
            `).join("");

    } catch (error) {

        container.innerHTML =
            "<p>Something went wrong.</p>";
    }
}