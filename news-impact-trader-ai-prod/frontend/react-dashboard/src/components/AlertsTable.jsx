import React from 'react';

export default function AlertsTable({alerts=[]}){
  return (
    <div>
      <h3>Alerts Table</h3>
      <table style={{width:'100%', color:'#fff'}}>
        <thead><tr><th>Ticker</th><th>Bias</th><th>Impact</th></tr></thead>
        <tbody>
          {alerts.map((a,i)=>(<tr key={i}><td>{a.ticker}</td><td>{a.bias}</td><td>{a.impact}</td></tr>))}
        </tbody>
      </table>
    </div>
  );
}
