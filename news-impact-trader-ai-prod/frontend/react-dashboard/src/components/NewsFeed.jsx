import React, {useEffect, useState} from 'react';
import axios from 'axios';

export default function NewsFeed(){
  const [news, setNews] = useState([]);
  useEffect(()=>{
    axios.get('http://localhost:8000/alerts').then(r=> setNews(r.data || [])).catch(()=>{});
  },[]);
  return (
    <div>
      <h3>Alerts</h3>
      <ul>{news.map((n,i)=>(<li key={i}>{n.ticker} - {n.bias} - {n.reason}</li>))}</ul>
    </div>
  );
}
