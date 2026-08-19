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
async function findCareerPath() {

    const roleSelect =
        document.getElementById("role-select");

    const resultsContainer =
        document.getElementById("career-results");

    const button =
        document.getElementById("career-button");

    const roleId =
        roleSelect.value;


    resultsContainer.innerHTML = `
        <div class="empty">
            <h3>Exploring career connections...</h3>
            <p>
                Finding roles connected through shared skills.
            </p>
        </div>
    `;


    button.disabled = true;


    try {

        const response = await fetch(
            `/api/role/${roleId}/career-path`
        );


        const data = await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Unable to load career paths."
            );
        }


        if (!data.results.length) {

            resultsContainer.innerHTML = `
                <div class="empty">

                    <h3>
                        No related roles found
                    </h3>

                    <p>
                        We couldn't find another role
                        sharing skills with this role.
                    </p>

                </div>
            `;

            return;
        }


        resultsContainer.innerHTML = `

            <div class="career-grid">

                ${data.results.map(role => `

                    <div class="career-card">

                        <div class="career-icon">
                            →
                        </div>

                        <div>

                            <h3>
                                ${role.title}
                            </h3>

                            <p class="muted">
                                ${role.overlap}
                                shared skill${role.overlap === 1 ? "" : "s"}
                            </p>

                            <div class="tags">

                                ${role.shared_skills
                                    .map(skill => `
                                        <span class="tag">
                                            ${skill}
                                        </span>
                                    `)
                                    .join("")
                                }

                            </div>

                        </div>

                    </div>

                `).join("")}

            </div>
        `;

    } catch (error) {

        resultsContainer.innerHTML = `

            <div class="error">

                <h3>
                    Unable to explore career paths
                </h3>

                <p>
                    ${error.message}
                </p>

            </div>

        `;

    } finally {

        button.disabled = false;

    }
}