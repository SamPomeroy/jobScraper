import { Link, useNavigate } from "react-router-dom";
import React, { useContext } from "react";
import "./Navbar.css";

import axios from "axios";
import Logo from "../../assets/Dev.svg";

import Horoscope from "../Horoscope/Horoscope";

const Navbar = () => {




    return (
        <>
           
                <div className='container-navbar'>
                    <div className="logo-container">
                        <img
                            src={Logo}
                            alt="My Logo"
                            className="logo"
                            title="Portifolio coming soon"
                        />
                    </div>
                    <nav>
                        
                         

                    </nav >
                </div >
                <Horoscope/>
            </>
        )
    }
    export default Navbar