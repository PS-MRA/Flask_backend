import React from "react"
import "./Toolbar.css"
import DrawerToggleButton from "../SideDrawer/DrawerToggleButton"
import logo from "../../Images/psg_logo.png"
const Toolbar = (props) => (
  <header className="toolbar">
    <nav className="toolbar_navigation">
      <div>
        <DrawerToggleButton click={props.drawerClickHandler} />
      </div>
      <div className="toolbar_logo">
        <a href="/">
          <img src={logo} alt="logo" style={{ height: "50px" }}></img>
        </a>
        {/* <a href="/">The LOGO</a> */}
      </div>
      <div className="space" />
      <div className="toolbar_navigation_items">
        <ul>
          <li>
            <a href="/">Products</a>
          </li>
          <li>
            <a href="/">Users</a>
          </li>
        </ul>
      </div>
    </nav>
  </header>
)

export default Toolbar
