import React from 'react';
import './Navbar.css';

import home from '../../../assets/home-button.svg';
import user from '../../../assets/user-button.svg';
import competition from '../../../assets/comp-button.svg'

const Navbar = () => {
    return (
        <div className='navbar-container'>
            <img src={home} alt='home' className='navbar-button'/>
            <img src={competition} alt='competition' className='navbar-button'/>
            <img src={user} alt='user' className='navbar-button'/>
        </div>
    )
}

export default Navbar;