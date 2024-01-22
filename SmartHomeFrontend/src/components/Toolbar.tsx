import '../css/Toolbar.css';

function Toolbar(){

    return (
        <ul className="menu">
            <li>
                <a href="/history">History</a>
            </li>
            <li>
                <a href="/">Home</a>
            </li>
        </ul>
    );
}

export default Toolbar;