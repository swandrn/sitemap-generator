import './Navbar.css';

function Navbar(): JSX.Element {
    return (
        <nav>
            <ul className="navbar">
                <li><a href="/">Home</a></li>
            </ul>
        </nav>
    )
}

export { Navbar }