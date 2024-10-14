import { Chart } from "react-google-charts";
import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import './Sitemap.css';

function sitemapToArr(sitemap: any) {
  let res = []
  for (let key in sitemap) {
    sitemap[key] = sitemap[key] == null ? "" : sitemap[key]
    let formattedKey = new URL(key).pathname
    res.push([
      {
        'v': key,
        'f': `<a href="${key}">${formattedKey}</a>`,
      },
      sitemap[key]
    ])
  }
  return res
}

function Sitemap() {
  const [sitemap, setSitemap] = useState([]);
  const [isLoading, setLoading] = useState(true);
  let [searchParams, _] = useSearchParams();
  useEffect(() => {
    if(isLoading){
      let queryUrl: string = 'http://localhost:8080/generate/sitemap?';
      searchParams.forEach((value, key) => {
        queryUrl = queryUrl.concat(`${key}=${value}`);
      });
      fetch(queryUrl, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => {
          if(response.ok){
            return response.json()
          }
          throw response;
        })
        .then(response => setSitemap(response))
        .catch(error => console.log(error))
        .finally(() => {
          setLoading(false);
        }) 
    }
  }, [])

  if(isLoading){
    return (
      <p>Loading...</p>      
    );
  }

  const chartData = sitemapToArr(sitemap)

  const options = {
    'allowCollapse': true,
    'allowHtml': true,
    'compactRows': true,
    'nodeClass': 'node',
    'selectedNodeClass': 'node-selected',
  }

  return (
    <Chart
      chartType="OrgChart"
      data={chartData}
      options={options}
      width="100%"
      height="100%"
    />
  );
}

export { Sitemap }
