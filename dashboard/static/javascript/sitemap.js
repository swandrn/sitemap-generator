const viewSitemap = document.querySelector('#view-sitemap')
google.charts.load('current', {packages:["orgchart"]});
google.charts.setOnLoadCallback(drawChart);

function sitemapToArr(sitemap){
    let res = []
    for(let key in sitemap){
        sitemap[key] = sitemap[key] == null ? "" : sitemap[key]
        let formattedKey = new URL(key).pathname
        res.push([
            {
                'v': key,
                'f': `<div class="node"><a href="${key}">${formattedKey}</a></div>`,
            },
            sitemap[key]
        ])
    }
    return res
}

function drawChart(){
    let chartData = sitemapToArr(JSON.parse(sitemapAsJson))
    console.log(chartData)
    let data = new google.visualization.DataTable()
    data.addColumn('string', 'Page')
    data.addColumn('string', 'Referer')
    
    data.addRows(chartData)
    
    let chart = new google.visualization.OrgChart(viewSitemap)
    
    chart.draw(data, {
        'allowCollapse': true,
        'allowHtml': true,
    })
}