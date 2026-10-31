import { useMemo, useState } from 'react';
import { Activity, ChevronDown, ChevronRight, Copy, Radio, Trash2 } from 'lucide-react';

const pretty = (value) => value == null ? '—' : typeof value === 'string' ? value : JSON.stringify(value, null, 2);
export default function HttpInspector({ entries, onClear }) {
  const [selectedId, setSelectedId] = useState(null);
  const [expanded, setExpanded] = useState(true);
  const selected = useMemo(() => entries.find(e => e.id === selectedId) || entries[0], [entries, selectedId]);
  const copy = async (value) => { try { await navigator.clipboard.writeText(pretty(value)); } catch { /* Clipboard may be unavailable on non-secure origins. */ } };
  return <section className="panel inspector-panel">
    <div className="panel-head inspector-head"><div className="title-with-icon"><div className="section-icon dark"><Activity size={18}/></div><div><h2>HTTP / Payload Inspector</h2><p>Traza de peticiones y respuestas en tiempo real</p></div></div><div className="inspector-actions"><span className="live-label"><Radio size={13}/> LIVE</span><button className="icon-button" title="Limpiar historial" onClick={onClear}><Trash2 size={16}/></button><button className="icon-button" title="Contraer panel" onClick={()=>setExpanded(v=>!v)}>{expanded?<ChevronDown size={17}/>:<ChevronRight size={17}/>}</button></div></div>
    {expanded && <>
      <div className="request-list">{entries.length===0 ? <div className="empty-inspector"><Activity size={24}/><span>Las solicitudes HTTP aparecerán aquí cuando interactúes con la API.</span></div> : entries.slice(0,12).map(entry=><button key={entry.id} className={`request-row ${selected?.id===entry.id?'selected':''}`} onClick={()=>setSelectedId(entry.id)}><span className={`method method-${entry.method.toLowerCase()}`}>{entry.method}</span><span className="request-url" title={entry.url}>{entry.url}</span><span className={`status-code ${entry.phase==='pending'?'pending':entry.status>=400||entry.status===0?'bad':'good'}`}>{entry.phase==='pending'?'…':entry.status||'ERR'}</span><span className="duration">{entry.durationMs==null?'—':`${entry.durationMs} ms`}</span></button>)}</div>
      {selected && <div className="inspector-detail"><div className="detail-meta"><span><b>{selected.method}</b> · {selected.url}</span><span className={`status-pill ${selected.status>=400||selected.status===0?'bad':'good'}`}>{selected.phase==='pending'?'En curso':`HTTP ${selected.status}`}</span></div><div className="payload-grid"><Payload title="Request Body" value={selected.requestBody} onCopy={copy}/><Payload title="Response Body" value={selected.responseBody} onCopy={copy}/></div></div>}
    </>}
  </section>;
}
function Payload({title,value,onCopy}) { return <div className="payload-card"><div className="payload-title"><span>{title}</span><button className="copy-button" onClick={()=>onCopy(value)} title="Copiar JSON"><Copy size={13}/> Copiar</button></div><pre>{pretty(value)}</pre></div>; }
