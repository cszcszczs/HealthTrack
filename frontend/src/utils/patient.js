export const EMPTY_PATIENT = {
  firstName: '', lastName: '', documentType: 'CEDULA', documentNumber: '', birthDate: '',
  gender: 'MASCULINO', email: '', phone: '', city: '', address: '',
};

export function toFormPatient(patient = {}) {
  return {
    ...EMPTY_PATIENT,
    ...patient,
    birthDate: patient.birthDate ? String(patient.birthDate).slice(0, 10) : '',
  };
}

export function toApiPatient(form) {
  return {
    firstName: form.firstName.trim(), lastName: form.lastName.trim(),
    documentType: form.documentType, documentNumber: form.documentNumber.trim(),
    birthDate: form.birthDate ? new Date(`${form.birthDate}T00:00:00.000Z`).toISOString() : '',
    gender: form.gender, email: form.email.trim(), phone: form.phone.trim(),
    city: form.city.trim(), address: form.address.trim(),
  };
}

export function unwrapPayload(result) { return result && Object.prototype.hasOwnProperty.call(result, 'payload') ? result.payload : result; }
