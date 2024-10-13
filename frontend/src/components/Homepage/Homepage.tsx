function Homepage() {
    return (
        <div>
            <h1>Sitemap Generator</h1>
            <form action="/generate/sitemap" method="get" >
                <label htmlFor="url-input">Generate sitemap from URL:</label>
                <input type="text" name="url" id="url-input" placeholder="https://example.com" />
                <label htmlFor="subdomain-radio">Limit crawling to current subdomain:</label>
                <input type="radio" name="subdomain_only" id="subdomain-radio" value="true" />
                <input type="submit" value="Generate Sitemap" />
            </form>
        </div >
    );
}

export {Homepage}