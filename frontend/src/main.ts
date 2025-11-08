/**
 * Application entry point
 */

import '@/assets/styles/main.css';
import { apiService } from '@/services';
import type { HelloResponse } from '@/types';

// Initialize app
const app = document.getElementById('app');

if (!app) {
  throw new Error('App element not found');
}

// Render UI
app.innerHTML = `
  <div class="container">
    <div class="card">
      <h1>Flask CI/CD Demo</h1>
      <p>This is a modern web application powered by <strong>TypeScript + Vite</strong> frontend and <strong>Flask</strong> backend.</p>
      <button id="callApi">Call Backend API</button>
      <div id="message"></div>
    </div>
    <div id="status"></div>
  </div>
`;

// Setup event handlers
const button = document.getElementById('callApi');
const messageEl = document.getElementById('message');

if (button && messageEl) {
  button.addEventListener('click', async () => {
    // Disable button during request
    button.setAttribute('disabled', 'true');
    messageEl.innerHTML = '<p class="message info">Loading...</p>';

    try {
      const response = await apiService.getHello();

      if (response.error) {
        messageEl.innerHTML = `<p class="message error">Error: ${response.error}</p>`;
      } else if (response.data) {
        const data = response.data as HelloResponse;
        messageEl.innerHTML = `
          <div class="message success">
            <p><strong>${data.message}</strong></p>
            <p style="margin-top: 8px; font-size: 14px;">
              Author: ${data.author}<br>
              Version: ${data.version}<br>
              Time: ${new Date(data.timestamp).toLocaleString()}
            </p>
          </div>
        `;
      }
    } catch (error) {
      messageEl.innerHTML = `<p class="message error">Failed to reach backend</p>`;
      console.error('API call failed:', error);
    } finally {
      button.removeAttribute('disabled');
    }
  });
}

// Check backend health on load
async function checkHealth() {
  const statusEl = document.getElementById('status');
  if (!statusEl) return;

  try {
    const response = await apiService.getHealth();
    if (response.data) {
      statusEl.innerHTML = `
        <p style="color: var(--color-text-secondary); font-size: var(--font-size-sm);">
          Backend Status: <strong style="color: var(--color-success);">${response.data.status}</strong>
        </p>
      `;
    }
  } catch (error) {
    statusEl.innerHTML = `
      <p style="color: var(--color-error); font-size: var(--font-size-sm);">
        Backend Status: <strong>Offline</strong>
      </p>
    `;
  }
}

// Run health check
checkHealth();
