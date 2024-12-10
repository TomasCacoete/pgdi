import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Navbar.css';

import home from '../../../assets/home.svg';
import user from '../../../assets/user-button.svg';
import competition from '../../../assets/list.svg'
import submit from '../../../assets/submission.svg'
import add from '../../../assets/add.svg'
import upload from '../../../assets/upload.svg'


const Navbar = () => {
    const navigate = useNavigate();
    return (
        <div className='navbar-container'>
            <img src={home} alt='home' className='navbar-button' onClick={()=>navigate('/competition')}/>
            <img src={submit} alt='submit' className='navbar-button' onClick={()=>navigate('/submission')}/>
            <img src={add} alt='add' className='navbar-button' onClick={()=>navigate('/create_competition')}/>
            <img src={user} alt='user' className='navbar-button' onClick={()=>navigate('/user')}/>
        </div>
    )
}

export default Navbar;