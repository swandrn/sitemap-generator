const viewSitemap = document.querySelector('#view-sitemap')
google.charts.load('current', {packages:["orgchart"]});
google.charts.setOnLoadCallback(drawChart);

/**
 * Iterate over an Object and create an array of the key value pair.
 * Returns an array of arrays
 * @param {object} sitemap 
 * @returns {Array<Array<object>>}
 */
function sitemapToArr(sitemap){
    console.log(sitemap)
    let res = []
    for(let key in sitemap){
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

function drawChart(){
    let chartData = sitemapToArr(JSON.parse(sitemapAsJson))
    let data = new google.visualization.DataTable()
    data.addColumn('string', 'Page')
    data.addColumn('string', 'Referer')
    
    data.addRows(chartData)
    
    let chart = new google.visualization.OrgChart(viewSitemap)
    
    chart.draw(data, {
        'allowCollapse': true,
        'allowHtml': true,
        'compactRows': true,
        'nodeClass': 'node',
        'selectedNodeClass': 'node-selected',
    })
}