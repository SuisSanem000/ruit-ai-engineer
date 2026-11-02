# Browsers, Automations (Playwright) & Chrome Extensions

> **From Luis's Email Cheat Sheet:** *"browsers, their automations, and chrome extensions"*

---

## 1. Browser Automation with Playwright

- **Why Playwright Is Better Than Older Tools (like Selenium):**
  - Selenium sends slow HTTP commands through an extra driver program.
  - **Playwright** talks directly to Chrome over a fast **WebSocket connection (Chrome DevTools Protocol / CDP)**.
- **Browser Contexts (Saving Memory & Time):**
  - Starting a full Chrome browser takes 1–2 seconds and lots of RAM.
  - Instead of opening 20 Chrome browsers, open **1 Chrome browser** and create 20 isolated **Browser Contexts** in milliseconds—each context has its own separate cookies, local storage, and proxy IP.
- **Smart Hybrid Automation (Do Not Click Every Button!):**
  - Clicking DOM buttons (`page.click()`) is slow and breaks whenever a website changes a CSS class.
  - **Better Way:**
    1. Block images, fonts, and videos (`page.route`) to cut residential proxy costs by 80% and load pages 3x faster.
    2. Use Playwright only to pass the initial anti-bot check (Cloudflare / DataDome) and get valid cookies, then run the actual API `fetch()` call directly inside the page context!
- **How Websites Detect Headless Browsers:**
  - Checking JavaScript flags like `navigator.webdriver === true`.
  - Checking **WebGL / Canvas graphics cards** (Linux servers have no real GPU, which reveals they are servers).
  - Checking datacenter IP addresses (AWS/Hetzner IPs get blocked; use residential proxies).

---

## 2. Chrome Extensions (Manifest V3)

- **Why Chrome Extensions Are Great for Ruit:**
  - When a seller installs the Ruit Chrome Extension on their own computer, they are **already logged into Vinted, Wallapop, Depop, and Facebook Marketplace** in their real Chrome browser.
  - Any action taken by the extension uses the seller's **real home IP address**, **real computer hardware fingerprint**, and **real login cookies**—so anti-bot systems rarely block it!
- **3 Parts of a Chrome Extension (Manifest V3):**
  - **1. Background Service Worker (`background.js`):**
    - Has permission to read cookies (`chrome.cookies`), open tabs, and talk to Ruit's backend server.
    - **Important Manifest V3 Quirk:** Chrome puts the Service Worker to sleep after ~30 seconds of no activity! Never save data in global JS variables—save state in **`chrome.storage.local`** and use **`chrome.alarms`** (or WebSocket heartbeats) to wake it up.
  - **2. Content Script (`content.js` — Isolated World):**
    - Runs inside the marketplace tab (`vinted.es`, `wallapop.com`) and can read or click the page DOM.
    - **Quirk:** It shares the HTML DOM with the page, but its JavaScript variables are **isolated** from the page's own JavaScript.
  - **3. Page `MAIN` World Script:**
    - If you need to read a JavaScript variable directly from the marketplace's own script (`window.__INITIAL_STATE__`), inject a small script into `world: "MAIN"` and pass the data back using `window.postMessage`.
- **Two Ways Ruit Can Use the Extension:**
  - **Cookie Sync:** The extension copies fresh login cookies from the seller's browser and sends them to Ruit's cloud servers so Celery workers can sync inventory 24/7.
  - **Direct Browser Execution:** For strict marketplaces (like Facebook Marketplace), Ruit's server sends a job to the extension over WebSocket, and the extension publishes or deletes the item directly inside the seller's browser.
