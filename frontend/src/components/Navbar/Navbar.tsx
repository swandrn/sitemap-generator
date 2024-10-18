import './Navbar.css';

function Navbar(): JSX.Element {
    return (
        <nav>
            <ul className="navbar">
                <li><h1 className="title">Sitemap Generator</h1></li>
                <li><a href="/">Home</a></li>
            </ul>
        </nav>
    )
}

export { Navbar }