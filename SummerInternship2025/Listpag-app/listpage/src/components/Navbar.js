import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import '../styles/Navbar.css'
import Avatar from '@mui/material/Avatar';
import { useEffect, useState } from 'react';
function Navbar(){
    const [message1,setMessage1]=useState('');
    useEffect(()=>{
      fetch('http://127.0.0.1:5000/retrieve',{method:"GET"})
        .then(response=>response.json())
        .then(data=>setMessage1(data.count))
      },[])
     return(
        <Box className='Navbar'>
            <AppBar position='static' id='Appbar'>
                <Toolbar id='Toolbar1'>
             <Typography id='PageTitle'>RFP Management</Typography>   
             <Typography id='Number' sx={{position:"relative",fontSize:"12px",right:"38%",color:"black"}}>{message1} Active RFPs</Typography>
             <Button id='NewRFP' color="inherit">+ New RFP</Button>
              <Tooltip title='Open Settings' >
                <Avatar  id='Profile' src=''/>
              </Tooltip>
             </Toolbar>
            </AppBar>
        </Box>
     )
}

export default Navbar;