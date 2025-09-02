import React from 'react';
import StockChart from './components/StockChart';
import NewsFeed from './components/NewsFeed';
import AlertsTable from './components/AlertsTable';

export default function App(){
  return (
    <div style={{padding:20, background:'#071021', color:'#fff', minHeight:'100vh'}}>
      <h1>News Impact Trader AI</h1>
      <div style={{display:'flex', gap:20}}>
        <div style={{flex:2}}><StockChart/></div>
        <div style={{flex:1}}><NewsFeed/><AlertsTable/></div>
      </div>
    </div>
  );
}
