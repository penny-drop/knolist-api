import React from "react";
import {Sidenav, Icon, Nav} from "rsuite";
import {Link, useLocation} from "react-router-dom";

function Sidebar() {
    let first = false;
    let second = false;
    let third = false;
    const location = useLocation()["pathname"];

    if (location === "/my-projects") first = true;
    else if (location === "/shared") second = true;
    else if (location === "/archived") third = true;

    return (
        <div style={{width: "17vw"}}>
            <Sidenav
                style={{height: "100vh", fontFamily: "Poppins", paddingTop: "3vh", paddingLeft: "1vh"}}>
                <Sidenav.Body>
                    <Nav>
                        <Link to="/my-projects">
                            <Nav.Item active={first} icon={<Icon icon="project"/>} componentClass="span">
                                My Projects
                            </Nav.Item>
                        </Link>
                        <Link to="/shared">
                            <Nav.Item active={second} icon={<Icon icon="people-group"/>} componentClass="span">
                                Shared with me
                            </Nav.Item>
                        </Link>
                        <Link to="/archived">
                            <Nav.Item active={third} icon={<Icon icon="archive"/>} componentClass="span">
                                Archived
                            </Nav.Item>
                        </Link>
                    </Nav>
                </Sidenav.Body>
            </Sidenav>
        </div>
    );
}

export default Sidebar;