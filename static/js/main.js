// Initialize Feather icons
feather.replace();

// Base API URL
const apiUrl = window.location.origin;

// Utility: Fetch data from the API
async function fetchData(endpoint) {
    try {
        const response = await fetch(`${apiUrl}/${endpoint}`);
        if (!response.ok) throw new Error(`Failed to fetch ${endpoint}`);
        return await response.json();
    } catch (error) {
        console.error(error);
        return [];
    }
}

// Populate Contacts
async function populateContacts() {
    const contacts = await fetchData('contacts');
    const listElement = document.querySelector('#chats .chat-list');
    listElement.innerHTML = '';
    contacts.forEach(contact => {
        const contactItem = document.createElement('li');
        contactItem.className = 'chat-item';
        contactItem.innerHTML = `
            <img src="${contact.avatar || 'https://via.placeholder.com/50'}" alt="${contact.name}'s Avatar">
            <div class="chat-details">
                <span class="name">${contact.name}</span>
                <span class="preview">${contact.phone}</span>
            </div>
        `;
        contactItem.addEventListener('click', () => showMessages(contact.name));
        listElement.appendChild(contactItem);
    });
}

// Show Messages (SMS)
async function showMessages(contactName) {
    const messages = await fetchData(`sms/${contactName}`);
    const chatWindow = document.querySelector('.chat-window');
    
    // Create chat header
    const header = document.createElement('div');
    header.className = 'chat-header';
    header.innerHTML = `
        <button class="btn btn-link" onclick="showSection('chats')">
            <i data-feather="arrow-left"></i>
        </button>
        <h4 class="mb-0 ms-3">${contactName}</h4>
    `;
    
    // Create messages container
    const messagesContainer = document.createElement('div');
    messagesContainer.className = 'd-flex flex-column flex-grow-1 overflow-auto';
    
    messages.forEach(msg => {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${msg.type}`;
        messageElement.innerHTML = `
            <p class="mb-1">${msg.text}</p>
            <span class="timestamp">${msg.time}</span>
        `;
        messagesContainer.appendChild(messageElement);
    });
    
    chatWindow.innerHTML = '';
    chatWindow.appendChild(header);
    chatWindow.appendChild(messagesContainer);
    chatWindow.style.display = 'flex';
    
    // Re-initialize Feather icons for new elements
    feather.replace();
}

// Show Call History
async function showCallHistory() {
    const calls = await fetchData('calls');
    const listElement = document.querySelector('#archived .archived-list');
    listElement.innerHTML = '';
    calls.forEach(call => {
        const callItem = document.createElement('li');
        callItem.className = 'chat-item';
        callItem.innerHTML = `
            <i data-feather="${call.type === 'incoming' ? 'phone-incoming' : 'phone-outgoing'}"></i>
            <div class="chat-details">
                <span class="name">${call.time}</span>
                <span class="preview">${call.duration} minutes</span>
            </div>
        `;
        listElement.appendChild(callItem);
    });
    feather.replace();
}

// Populate Settings
async function populateSettings() {
    const settings = await fetchData('settings');
    const settingsContainer = document.getElementById('settings-content');
    settingsContainer.innerHTML = `
        <img src="${settings.account.avatar || 'https://via.placeholder.com/100'}" alt="Profile Picture">
        <h3>${settings.account.name}</h3>
        <div class="form-check form-switch mb-3">
            <input class="form-check-input" type="checkbox" id="activeStatus" ${settings.activeStatus ? 'checked' : ''}>
            <label class="form-check-label" for="activeStatus">Active Status</label>
        </div>
        <div class="form-check form-switch mb-3">
            <input class="form-check-input" type="checkbox" id="notifications" ${settings.notifications.notificationSounds ? 'checked' : ''}>
            <label class="form-check-label" for="notifications">Notification Sounds</label>
        </div>
        <div class="form-check form-switch mb-3">
            <input class="form-check-input" type="checkbox" id="darkMode" ${settings.darkMode === 'on' ? 'checked' : ''}>
            <label class="form-check-label" for="darkMode">Dark Mode</label>
        </div>
    `;
}

// Show Specific Section
function showSection(sectionId) {
    const sections = document.querySelectorAll('.section');
    const chatWindow = document.querySelector('.chat-window');
    sections.forEach(section => section.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
    chatWindow.style.display = 'none';
}

// Setup Sidebar Navigation
function setupSidebar() {
    const sidebarItems = document.querySelectorAll('.sidebar li');
    sidebarItems.forEach(item => {
        item.addEventListener('click', () => {
            const sectionId = item.dataset.section;
            showSection(sectionId);
            if (sectionId === 'chats') populateContacts();
            else if (sectionId === 'archived') showCallHistory();
            else if (sectionId === 'settings') populateSettings();
        });
    });
}

// Setup Search
function setupSearch() {
    const searchInput = document.getElementById('search');
    searchInput.addEventListener('input', async () => {
        const searchTerm = searchInput.value.toLowerCase();
        const contacts = await fetchData('contacts');
        const filteredContacts = contacts.filter(contact =>
            contact.name.toLowerCase().includes(searchTerm) ||
            contact.phone.toLowerCase().includes(searchTerm)
        );
        const listElement = document.querySelector('#chats .chat-list');
        listElement.innerHTML = '';
        filteredContacts.forEach(contact => {
            const contactItem = document.createElement('li');
            contactItem.className = 'chat-item';
            contactItem.innerHTML = `
                <img src="${contact.avatar || 'https://via.placeholder.com/50'}" alt="${contact.name}'s Avatar">
                <div class="chat-details">
                    <span class="name">${contact.name}</span>
                    <span class="preview">${contact.phone}</span>
                </div>
            `;
            contactItem.addEventListener('click', () => showMessages(contact.name));
            listElement.appendChild(contactItem);
        });
    });
}

// Initialize Application
async function initializeApp() {
    setupSidebar();
    setupSearch();
    await populateContacts();
}

// Start the app
document.addEventListener('DOMContentLoaded', initializeApp);
