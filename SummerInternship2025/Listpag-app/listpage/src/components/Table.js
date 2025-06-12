import Table from '@mui/material/Table';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import { useEffect, useState } from 'react';
import { Dialog, DialogContent, TableBody } from '@mui/material';
import Typography from '@mui/material/Typography';
import VisibilityIcon from '@mui/icons-material/Visibility';
import EditIcon from '@mui/icons-material/Edit';
import IconButton from '@mui/material/IconButton';
import {Stack} from '@mui/material';
import {Modal} from '@mui/material'
import EditPage from '../pages/editpage';
// import '../styles/Table.css'
import Popover from '@mui/material/Popover';
export default function Tablefunc(){
  const style={fontWeight:"bold",width:"20%"}
  const style1={fontWeight:"bold",width:"50%"}
  const [message,setMessage]=useState([]);
  useEffect(()=>{
    fetch('http://127.0.0.1:5000/retrieve',{method:"GET"})
      .then(response=>response.json())
      .then(data=>setMessage(data.message))
    },[])
  const style4 = {
    verticalScrollOnly: {
    overflowY: 'auto',
    overflowX: 'hidden',
    maxHeight: '80vh', // or any value suitable for your layout
  },
  
  }
    const [open, setOpen] = useState(false);
    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false); 
    console.log(message)
    return(<Box className='RFPTable'>
    <TableContainer id='Tabcontainer' sx={{width: '95%',position: 'relative',left:'2%'}} component={Paper}>
      <Table id='RFP' >
        <TableHead>
          <TableRow>
            <TableCell className='Heading' sx={style} >RFP Title</TableCell>
            <TableCell className='Heading' sx={style} align="left">Department</TableCell>
            <TableCell className='Heading' sx={style} align="left">Type&nbsp;</TableCell>
            <TableCell className='Heading' sx={style} align="left">Priority&nbsp;</TableCell>
            <TableCell className='Heading' sx={style} align="left">Amount&nbsp;</TableCell>
            <TableCell className='Heading' sx={style1} align="left">Key Dates&nbsp;</TableCell>
            <TableCell className='Heading' sx={style} align="left">Documents&nbsp;</TableCell>
            <TableCell className='Heading' sx={style} align="left">Updates&nbsp;</TableCell>
            <TableCell className='Heading' sx={style} align="left">Actions&nbsp;</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {message.map((row) => (
            <TableRow
              key={row.title[0]}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
              <Typography id='Title' sx={{fontSize:"15px",fontWeight:"bold",whiteSpace:"nowrap"}}>
              {row.title[0]}</Typography>
              <Typography sx={{fontSize:"12px",color:"grey",whiteSpace:"nowrap"}} id='Description'>
              {row.title[1]}
              </Typography>
              </TableCell>
              <TableCell sx={{whiteSpace:"nowrap"}} align="left">{row.department}</TableCell>
              <TableCell  align="left">{row.rfp_type}</TableCell>
              <TableCell align="left">{row.priority}</TableCell>
              <TableCell align="left">{row.amount}</TableCell>
              <TableCell  align="left">
              <Typography sx={{whiteSpace:"nowrap",fontWeight:"Bold",fontSize:"13px",color:"grey"}}>Deadline:  
              <Typography component="span" sx={{ color: "red",fontWeight:"Bold", fontSize: "13px" }}>
              {row.deadline}
              </Typography>
              </Typography>
              <Typography sx={{whiteSpace:"nowrap",fontWeight:"Bold",fontSize:"13px",color:"grey"}}>Submit:
              <Typography component="span" sx={{ color: "black",fontWeight:"Bold", fontSize: "13px" }}>
              {row.Submit}
              </Typography>
              </Typography>
              </TableCell>
              <TableCell align="left">{"Not yet implemented"}</TableCell>
              <TableCell align="left">{"Not yet implemented"}</TableCell>
              <TableCell align="left"><Stack direction={'row'} ><IconButton color='primary' size='small' >
                <VisibilityIcon/>
                </IconButton>
                <IconButton color='inherit' size='small' onClick={handleOpen}>
                  <EditIcon/>
                  </IconButton>
              <Dialog 
          fullWidth
          open={open}
          style={style4}
          scroll='paper'
        onClose={handleClose}
        aria-labelledby="edit-modal-title"
        aria-describedby="edit-modal-description">
          <DialogContent  sx={{p:0,".MuiDialog-paper::-webkit-scrollbar:horizontal":{ display:"none"}}}>
          <EditPage onClose={handleClose} />
          </DialogContent>
        </Dialog>
              </Stack>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
        </Table>
    </TableContainer>
    </Box>)
}