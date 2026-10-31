import axios from 'axios';

let inspectorCallback = () => {};
export const setInspectorCallback = (callback) => { inspectorCallback = callback || (() => {}); };

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:7000',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
});

// Metadata is attached to each request so the response interceptor can calculate duration.
http.interceptors.request.use((config) => {
  config.metadata = { startedAt: performance.now(), requestBody: config.data ?? null };
  inspectorCallback({
    id: `${Date.now()}-${Math.random()}`, phase: 'pending', method: (config.method || 'get').toUpperCase(),
    url: `${config.baseURL || ''}${config.url || ''}`, requestBody: config.data ?? null,
    responseBody: null, status: null, durationMs: null, timestamp: new Date().toISOString(),
  });
  return config;
});

const report = (config, response, error = null) => {
  const startedAt = config?.metadata?.startedAt;
  inspectorCallback({
    id: `${Date.now()}-${Math.random()}`, phase: error ? 'error' : 'complete',
    method: (config?.method || 'get').toUpperCase(), url: `${config?.baseURL || http.defaults.baseURL}${config?.url || ''}`,
    requestBody: config?.metadata?.requestBody ?? config?.data ?? null,
    responseBody: response?.data ?? error?.response?.data ?? { error: error?.message || 'Error desconocido' },
    status: response?.status ?? error?.response?.status ?? 0,
    durationMs: startedAt == null ? null : Math.round(performance.now() - startedAt),
    timestamp: new Date().toISOString(),
  });
};

http.interceptors.response.use(
  (response) => { report(response.config, response); return response; },
  (error) => { report(error.config, error.response, error); return Promise.reject(error); },
);

export default http;
