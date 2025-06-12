// login.js page
import '../styles/login.css'
import Button from '@mui/material/Button';
import { Box,TextField,FormControl } from '@mui/material';
import { Link } from "react-router-dom";
import React, {  useState } from 'react';
function Formtemp(){
const [Username,setUsername]=useState('')
const [Password,setPassword]=useState('')
const [message,setMessage]=useState('')
const Authorization = async() =>{
       fetch("http://127.0.0.1:8081/login",
        {
            method:"POST",
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify({Username,Password})
        })
        // const data = await response.json()
        .then(response=>response.json())
        .then(data=>setMessage(data.message))
        .catch((error)=>console.error(error))
}

    return (
            <Box className="Page-Details"> 
                <h2 id='Heading'>Login</h2>
            <FormControl id='Form Details'>
                {/* <label className='Txtlab'>Username</label> */}
                <TextField className='input' id='Username'  value={Username}  onChange={(e) => setUsername(e.target.value)}  label='Username' required></TextField>
                <br></br><br></br>
                {/* <label className='Txtlab'>Password</label> */}
                <TextField className='input' id='Password' value={Password} onChange={(e) => setPassword(e.target.value)} type='Password' label='Password' required></TextField>
                <Link id='fp1' to='/ForgetPassword' ><h5 id='forgotpass'>Forgot Password</h5></Link>
                <Button id='login' onClick={Authorization} variant="contained" color="primary">Login</Button>
            </FormControl>

            <h5 id='Cracc'>Create Account</h5>
            <h5 id='FinalAuthmessage'>{message}</h5>
            </Box>
    )
}

export default Formtemp;

