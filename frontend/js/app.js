const API_URL = "http://localhost:8000/api/search";

const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const resultsContainer = document.getElementById('results');

async function doSearch() {
    const query = searchInput.value.trim();
    if (!query) return;

    // Show loading state (simple opacitiy change for now)
    resultsContainer.style.opacity = '0.5';

    try {
        const response = await fetch(`${API_URL}?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        renderResults(data);
    } catch (error) {
        console.error('Error:', error);
        resultsContainer.innerHTML = '<p class="empty-state">Ocurrió un error. Intenta de nuevo.</p>';
    } finally {
        resultsContainer.style.opacity = '1';
    }
}

function renderResults(data) {
    resultsContainer.innerHTML = '';

    // Combine albums and tracks or show sections? Let's mix them or prioritize albums for now.
    // Let's show Albums first

    if (data.albums.length === 0 && data.tracks.length === 0) {
        resultsContainer.innerHTML = '<p class="empty-state">No se encontraron resultados.</p>';
        return;
    }

    // Render Albums
    data.albums.forEach(album => {
        const card = document.createElement('div');
        card.className = 'card animation-fade-in';

        const imageUrl = album.images[0]?.url || 'https://via.placeholder.com/300/000000/FFFFFF/?text=No+Image';
        const artistName = album.artists[0]?.name || 'Unknown Artist';

        card.innerHTML = `
            <img src="${imageUrl}" alt="${album.name}" loading="lazy">
            <div class="card-info">
                <div class="card-title" title="${album.name}">${album.name}</div>
                <div class="card-subtitle">Álbum • ${artistName}</div>
            </div>
        `;

        // Add click listener if we want to do something later
        resultsContainer.appendChild(card);
    });
}

// Event Listeners
searchBtn.addEventListener('click', doSearch);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') doSearch();
});

