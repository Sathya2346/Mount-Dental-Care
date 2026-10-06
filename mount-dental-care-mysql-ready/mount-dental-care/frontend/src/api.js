import axios from "axios";

const defaultHost = (typeof window !== "undefined" && window.location.hostname) ? window.location.hostname : "127.0.0.1";

// Where the API lives:
//   * VITE_API_BASE when set (explicit override, e.g. a separate API domain).
//   * the Django dev server on port 8000 while running `npm run dev` locally.
//   * "/api" everywhere else — in production Django serves this bundle itself
//     (config/urls.py: serve_react), so the same origin answers and no CORS
//     setup is needed on the host.
function resolveApiBase() {
  if (import.meta.env.VITE_API_BASE) return import.meta.env.VITE_API_BASE;
  // Localhost on any port other than Django's own 8000 is the Vite dev
  // server (5173 by default, 5174 when that port is taken).
  const isLocalDev = typeof window !== "undefined"
    && ["localhost", "127.0.0.1", "[::1]"].includes(window.location.hostname)
    && window.location.port !== "8000";
  return isLocalDev ? `http://${defaultHost}:8000/api` : "/api";
}

export const API_BASE = resolveApiBase();
export const api = axios.create({
  baseURL: API_BASE,
  timeout: 15000
});

// Convert Django media paths to browser-safe absolute URLs.
export function mediaUrl(value) {
  if (!value) return null;
  const str = String(value).trim();
  if (!str) return null;
  const origin = API_BASE.replace(/\/api\/?$/, "");
  if (/^https?:\/\/(?:localhost|127\.0\.0\.1):8000\//i.test(str)) {
    return str.replace(/^https?:\/\/(?:localhost|127\.0\.0\.1):8000/i, origin);
  }
  if (/^https?:\/\//i.test(str)) return str;
  return `${origin}/${str.replace(/^\/+/, "")}`;
}

export function setToken(token) {
  if (token) localStorage.setItem("mdc_access", token);
  else localStorage.removeItem("mdc_access");
}
export function getToken() { return localStorage.getItem("mdc_access"); }
api.interceptors.request.use(config => {
  const token=getToken();
  if(token) config.headers.Authorization=`Bearer ${token}`;
  return config;
});

const AUTH_ENDPOINTS = ["/auth/login/", "/auth/register/"];

// A stale access token in localStorage (expired, or signed with an older
// SECRET_KEY) makes every request fail with 401 — which silently broke the CMS
// refresh, the booking form and the OTP email flow. Drop the dead token and
// retry once without it so public endpoints keep working.
api.interceptors.response.use(
  response => response,
  error => {
    const config = error?.config;
    const isAuthCall = AUTH_ENDPOINTS.some(path => (config?.url || "").includes(path));
    if (error?.response?.status === 401 && getToken() && config && !isAuthCall && !config._retriedWithoutAuth) {
      setToken(null);
      config._retriedWithoutAuth = true;
      if (config.headers) delete config.headers.Authorization;
      return api.request(config);
    }
    return Promise.reject(error);
  }
);
export async function loadSite(){
  // Prevent the browser from serving an old CMS response after an admin edit.
  return (await api.get("/site/", { params: { _ts: Date.now() } })).data;
}
export async function requestAppointmentOtp(payload){ return (await api.post("/appointments/request-otp/",payload)).data; }
export async function verifyAppointmentOtp(payload){ return (await api.post("/appointments/verify-otp/",payload)).data; }
export async function loginUser(payload){ const d=(await api.post("/auth/login/",payload)).data; setToken(d.access); return d; }
export async function registerUser(payload){ const d=(await api.post("/auth/register/",payload)).data; setToken(d.access); return d; }
export async function dashboard(){ return (await api.get("/user/dashboard/")).data; }
export function logoutUser(){ setToken(null); }
