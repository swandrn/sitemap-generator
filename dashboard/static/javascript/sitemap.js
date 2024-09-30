const viewSitemap = document.querySelector('#view-sitemap')
let treeDiagram = echarts.init(viewSitemap)

function createSitemapAsObj(data){
    sitemapAsObj = []
    for(let key in data){
        urlsAsObj = {
            pageurl: key,
            parenturl: data[key]
        }
        sitemapAsObj.push(urlsAsObj)
    }
    return sitemapAsObj
}

function createFlatTreeData(groupedUrls){
    let flatTreeData = []
    for(let key in groupedUrls){
        dataObj = {
            name: key,
            children: [],
        }
        for(let obj = 0; obj < groupedUrls[key].length; obj++){
            dataObj.children.push({name: groupedUrls[key][obj].pageurl})
        }
        flatTreeData.push(dataObj)
    }
    return flatTreeData
}

function getObjectByValue(obj, value) {
    let result = null
    if(obj instanceof Array) {
        for(let i = 0; i < obj.length; i++) {
            result = getObjectByValue(obj[i], value)
            if (result) {
                break
            }  
        }
    } else {
        for(let prop in obj) {
            if(obj[prop] == value && Object.hasOwn(obj, 'children')) {
                return obj
            }
            if(obj[prop] instanceof Array) {
                result = getObjectByValue(obj[prop], value)
                if (result) {
                    break
                }
            } 
        }
    }
    return result
}

// function normalizeUrl(url) {
//     return url.replace(/\/+$/, '');
// }

function createTreeData(node, nodes, visited = new Set()) {
    if (visited.has(node.name)) {
        return node
    }
    
    visited.add(node.name)

    if (node.children) {
        node.children = node.children.map(child => {
            const childNode = getObjectByValue(nodes, child.name)
            if (childNode) {
                return createTreeData(childNode, nodes, visited)
            }
            return child
        })
    }
    
    return node
}

arraySitemapAsObj = createSitemapAsObj(JSON.parse(sitemapAsJson))

let groupedUrls = Object.groupBy(arraySitemapAsObj, obj => {
    return obj.parenturl
})

let flatTreeData = createFlatTreeData(groupedUrls)

const nullValue = getObjectByValue(flatTreeData, 'null')
const rootNode = getObjectByValue(flatTreeData, nullValue.children[0].name)
const data = [createTreeData(rootNode, flatTreeData)];

console.log(data)

let option = {
    tooltip: {
        trigger: 'item',
        triggerOn: 'mousemove',
    },
    grid: {
        left: '50',
    },
    series: [
        {
            type: 'tree',
            id: 0,
            name: 'tree1',
            data: data,
            top: '10%',
            left: '8%',
            bottom: '22%',
            right: '20%',
            symbolSize: 7,
            edgeShape: 'polyline',
            edgeForkPosition: '63%',
            initialTreeDepth: 3,
            lineStyle: {
                width: 2
            },
            label: {
                backgroundColor: '#fff',
                position: 'left',
                verticalAlign: 'middle',
                align: 'right'
            },
            leaves: {
                label: {
                    position: 'right',
                    verticalAlign: 'middle',
                    align: 'left'
                }
            },
            emphasis: {
                focus: 'descendant'
            },
            expandAndCollapse: true,
            animationDuration: 550,
            animationDurationUpdate: 750
        }
    ]
}

treeDiagram.setOption(option)