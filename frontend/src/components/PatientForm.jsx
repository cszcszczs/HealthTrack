import { useEffect, useState } from 'react';
import { Save, X, UserRoundPlus } from 'lucide-react';
import { EMPTY_PATIENT, toFormPatient, toApiPatient } from '../utils/patient';

const fields = [
  ['firstName','Nombres','text',true], ['lastName','Apellidos','text',true],
  ['documentNumber','Número de documento','text',true], ['birthDate','Fecha de nacimiento','date',true],
  ['email','Correo electrónico','email',true], ['phone','Teléfono','tel',true],
  ['city','Ciudad','text',true], ['address','Dirección','text',true],
];

export default function PatientForm({ patient, onSubmit, onCancel, busy }) {
  const [form, setForm] = useState(toFormPatient(patient || EMPTY_PATIENT));
  useEffect(() => setForm(toFormPatient(patient || EMPTY_PATIENT)), [patient]);
  const change = (e) => setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
  const submit = (e) => { e.preventDefault(); onSubmit(toApiPatient(form)); };
  return <form className="patient-form" onSubmit={submit}>
    <div className="form-heading"><div className="section-icon"><UserRoundPlus size={18}/></div><div><h3>{patient ? 'Editar paciente' : 'Registrar paciente'}</h3><p>{patient ? 'Actualiza los datos del registro seleccionado.' : 'Completa la información para crear un registro.'}</p></div></div>
    <div className="form-grid">
      {fields.slice(0,2).map(([name,label,type,required]) => <label className="field" key={name}>{label}<input name={name} type={type} value={form[name]} onChange={change} required={required} maxLength={100}/></label>)}
      <label className="field">Tipo de documento<select name="documentType" value={form.documentType} onChange={change}><option value="CEDULA">Cédula</option><option value="PASAPORTE">Pasaporte</option><option value="TARJETA_IDENTIDAD">Tarjeta de identidad</option><option value="CEDULA_EXTRANJERIA">Cédula de extranjería</option></select></label>
      {fields.slice(2,4).map(([name,label,type,required]) => <label className="field" key={name}>{label}<input name={name} type={type} value={form[name]} onChange={change} required={required} maxLength={name==='documentNumber'?30:undefined}/></label>)}
      <label className="field">Género<select name="gender" value={form.gender} onChange={change}><option value="MASCULINO">Masculino</option><option value="FEMENINO">Femenino</option><option value="OTRO">Otro</option><option value="NO_ESPECIFICADO">Prefiere no decir</option></select></label>
      {fields.slice(4).map(([name,label,type,required]) => <label className={`field ${name==='address'?'full':''}`} key={name}>{label}<input name={name} type={type} value={form[name]} onChange={change} required={required} maxLength={name==='address'?200:100}/></label>)}
    </div>
    <div className="form-actions"><button type="button" className="btn btn-secondary" onClick={onCancel}><X size={16}/> Cancelar</button><button className="btn btn-primary" disabled={busy}><Save size={16}/>{busy?'Enviando…':patient?'Guardar cambios':'Crear paciente'}</button></div>
  </form>;
}
