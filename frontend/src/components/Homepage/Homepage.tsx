import './Homepage.css';

function Homepage(): JSX.Element {
    return (
        <div>
            <form action="/generate/sitemap" method="get" >
                <label htmlFor="url-input">Generate sitemap from URL:</label>
                <input type="text" name="url" id="url-input" className="text-input" placeholder="https://example.com" />
                <label htmlFor="subdomain-checkbox" className="control control--checkbox">Limit crawling to current subdomain:
                    <input type="checkbox" name="subdomain_only" id="subdomain-checkbox" value="true" />
                    <div className="control__indicator"></div>
                </label>
                <input type="submit" className="button" value="Generate Sitemap" />
            </form>
        </div >
    );
}

export { Homepage }