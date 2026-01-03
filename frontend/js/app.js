// Configuración de API URL
// Si estamos en local, usa el puerto 8000. Si estamos en producción (ej. Render, Vercel), usa la URL relativa o la que definas.
// Para este setup, asumiremos que en producción el usuario configurará la URL del backend manualmente o usará el mismo dominio si sirve ambos.
// Una estrategia común simple para separar frontend/backend en servicios gratuitos:
const IS_LOCAL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_URL = IS_LOCAL
    ? "http://localhost:8000/api/search"
    : "https://south-sounds-explorer.onrender.com";

const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const resultsContainer = document.getElementById('results');
const genreChips = document.querySelectorAll('.chip');
const tabBtns = document.querySelectorAll('.tab-btn');
const loadMoreBtn = document.getElementById('loadMoreBtn'); // New

let currentSort = 'best';
let currentPage = 1;
let lastQuery = "";

async function doSearch(queryOverride = null, nextPage = false) {
    let query = queryOverride !== null ? queryOverride : searchInput.value.trim();

    // Logic to handle new search vs pagination
    if (!nextPage) {
        currentPage = 1;
        lastQuery = query;
        resultsContainer.innerHTML = ''; // Clear only on new search
        loadMoreBtn.classList.add('hidden');
    } else {
        query = lastQuery; // Use saved query for pagination
    }

    // Show loading state
    if (!nextPage) resultsContainer.style.opacity = '0.5';
    // If paging, maybe change button text?
    if (nextPage) loadMoreBtn.textContent = 'Cargando...';

    try {
        const url = new URL(API_URL);
        if (query) url.searchParams.append('q', query);
        url.searchParams.append('sort_by', currentSort);
        url.searchParams.append('page', currentPage);

        const response = await fetch(url);
        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        renderResults(data, nextPage);

        // Pagination logic: if we got less than 20 results (our limit), probably no more pages.
        // Discogs returns 100 per page, but we filter. 
        // If we found any results, show Load More (optimistic). 
        // A better way would be checking 'pagination' object from API if we exposed it, but for now:
        if (data.releases && data.releases.length > 0) {
            loadMoreBtn.classList.remove('hidden');
        } else {
            loadMoreBtn.classList.add('hidden');
        }

    } catch (error) {
        console.error('Error:', error);
        if (!nextPage) resultsContainer.innerHTML = '<p class="empty-state">Ocurrió un error. Intenta de nuevo.</p>';
    } finally {
        resultsContainer.style.opacity = '1';
        loadMoreBtn.textContent = 'Cargar más';
    }
}

function renderResults(data, append = false) {
    const releases = data.releases || [];

    if (releases.length === 0) {
        if (!append) resultsContainer.innerHTML = '<p class="empty-state">No se encontraron resultados en Latam.</p>';
        return;
    }

    releases.forEach(release => {
        const card = document.createElement('div');
        card.className = 'card animation-fade-in';

        const imageUrl = release.thumb || release.cover_image || 'https://via.placeholder.com/300/0f0f13/FFFFFF/?text=No+Cover';
        const year = release.year ? ` • ${release.year}` : '';
        const country = release.country ? ` • ${release.country}` : '';
        const style = release.style ? release.style.slice(0, 2).join(", ") : 'Electronic';

        card.innerHTML = `
            <img src="${imageUrl}" alt="${release.title}" loading="lazy" onerror="this.src='https://via.placeholder.com/300/0f0f13/FFFFFF/?text=No+Image'">
            <div class="card-info">
                <div class="card-title" title="${release.title}">${release.title}</div>
                <div class="card-subtitle">${style}</div>
                <div class="card-subtitle small" style="margin-top:4px; font-size:0.8rem; opacity:0.7">
                    ${release.format ? release.format[0] : 'Release'}${year}${country}
                </div>
            </div>
        `;

        if (release.uri) {
            card.onclick = () => window.open(`https://www.discogs.com${release.uri}`, '_blank');
        }

        resultsContainer.appendChild(card);
    });
}

// Event Listeners

// 1. Search
searchBtn.addEventListener('click', () => doSearch());
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') doSearch();
});

// 2. Genre Chips (Dynamic)
// 2. Genre & Country Chips (Dynamic)
const genreChipsContainer = document.getElementById('genreChipsContainer');
const countryChipsContainer = document.getElementById('countryChipsContainer');

async function loadSuggestions() {
    // Lead Genres
    try {
        const response = await fetch(`${API_URL}/genres`);
        const data = await response.json();
        const genres = data.genres || [];

        genreChipsContainer.innerHTML = '';
        genres.forEach(genre => {
            const btn = document.createElement('button');
            btn.className = 'chip animation-fade-in';
            btn.textContent = genre;
            btn.addEventListener('click', () => {
                searchInput.value = genre;
                doSearch(genre);
            });
            genreChipsContainer.appendChild(btn);
        });
    } catch (e) { console.error(e); }

    // Load Countries
    try {
        const response = await fetch(`${API_URL}/countries`);
        const data = await response.json();
        const countries = data.countries || [];

        countryChipsContainer.innerHTML = '';
        countries.forEach(country => {
            const btn = document.createElement('button');
            btn.className = 'chip animation-fade-in';
            btn.textContent = country;
            btn.addEventListener('click', () => {
                searchInput.value = country;
                // Just searching by Text will work fine for countries
                doSearch(country);
            });
            countryChipsContainer.appendChild(btn);
        });
    } catch (e) { console.error(e); }
}

// 3. Tabs
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentSort = btn.dataset.sort;
        doSearch();
    });
});

// 4. Load More
loadMoreBtn.addEventListener('click', () => {
    currentPage++;
    doSearch(null, true);
});

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
    loadSuggestions();
    doSearch("");
});

// 5. Scroll to Top
const scrollTopBtn = document.getElementById('scrollTopBtn');

window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        scrollTopBtn.classList.add('visible');
        scrollTopBtn.classList.remove('hidden');
    } else {
        scrollTopBtn.classList.remove('visible');
        scrollTopBtn.classList.add('hidden');
    }
});

scrollTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});
