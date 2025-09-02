import React from 'react';
import { AdvancedChart } from 'react-tradingview-embed';

export default function StockChart(){
  return (
    <div style={{height:600}}>
      <AdvancedChart widgetProps={{ symbol: 'NSE:RELIANCE', theme:'dark', interval:'D', autosize:true }}/>
    </div>
  );
}
