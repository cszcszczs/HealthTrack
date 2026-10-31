import http from './http';

// API response examples wrap records in { operacion, payload }.
const unwrap = (response) => response.data;
export const patientsApi = {
  async list() { return unwrap(await http.get('/api/patients')); },
  async getById(id) { return unwrap(await http.get(`/api/patients/${encodeURIComponent(id.trim())}`)); },
  async create(patient) { return unwrap(await http.post('/api/patients', patient)); },
  async update(id, patient) { return unwrap(await http.put(`/api/patients/${encodeURIComponent(id.trim())}`, patient)); },
  async deactivate(id) { return unwrap(await http.delete(`/api/patients/${encodeURIComponent(id.trim())}`)); },
};
