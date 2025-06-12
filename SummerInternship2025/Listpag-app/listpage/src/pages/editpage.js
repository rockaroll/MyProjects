import { FormControl,TextField,Button,Box,Typography,Autocomplete,Stack,Divider,TextareaAutosize, IconButton } from "@mui/material";
import { DesktopDatePicker} from "@mui/x-date-pickers";
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import BackupIcon from '@mui/icons-material/Backup';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import CloseIcon from '@mui/icons-material/Close';
export default function EditPage(){
    return( <Box className='Edit' sx={{display: 'grid',alignItems: 'center', flexWrap: 'wrap'}}>
        <Stack direction={"row"} spacing={3} style={{marginBottom:"2%",marginTop:"2%",display:"flex",alignItems:"center"}}>
         <Typography id='Pageheading' sx={{position:"relative",left:"2%",marginTop:"2%",marginBottom:"2%",color:"black"}}>Edit RFP</Typography>
         <IconButton color="error"  style={{position:"relative",left:"76%"}}><CloseIcon/></IconButton>
        </Stack> 
         <Divider sx={{ bgcolor: 'background.paper'}} />
         <FormControl sx={{marginLeft:"2%",marginTop:"1%"}} id='ChangeParams'>
            <Typography>RFP Title *</Typography>
                <TextField sx={{width:"95%",'& .MuiInputBase-input': {height:"5px",boxSizing: 'border-box'}}} ></TextField>
                <br></br>
                <Stack direction={"row"} spacing={23.3}>
                <Typography>Department *</Typography>
                <Typography sx={{}}>RFP Type *</Typography>
                </Stack>
                <Stack direction={"row"} spacing={3}>
                <Autocomplete id='DepartmentField' disablePortal options={['IT Department','All Departments','HR Department','Finance','Marketing']}  renderInput={(params) => <TextField  sx={{width:"260px",'& .MuiInputBase-input': {height:"5px",boxSizing: 'border-box'}}} {...params}  placeholder="Select Department" required />}  />
                <Autocomplete id='TypeField' disablePortal options={['Services','Licences']}  renderInput={(params) => <TextField  sx={{width:"260px",'& .MuiInputBase-input': {height:"5px",boxSizing: 'border-box'}}} {...params}  placeholder="Select Types" required />}  />
               </Stack>
               <br></br>
               <Stack direction={"row"} spacing={27.5}>
                <Typography>Priority *</Typography>
                <Typography sx={{}}>Budget Amount *</Typography>
                </Stack>
                <Stack direction={"row"} spacing={3}>
                <Autocomplete id='PriorityField' disablePortal options={['Low','Medium','High']}  renderInput={(params) => <TextField  sx={{width:"260px",'& .MuiInputBase-input': {height:"5px",boxSizing: 'border-box'}}} {...params}  placeholder="Select Department" required />}  />
                <TextField sx={{width:"260px",'& .MuiInputBase-input': {height:"5px",boxSizing: 'border-box'}}}></TextField>
                </Stack>
                <br></br>
                <Typography>Description</Typography>
                <TextareaAutosize  minRows={3}  style={{width:"94%"}}/>
                  <br></br>
                 <Typography>Attach Documents</Typography>
                <Box sx={{border:"1px dashed grey",width:"95%"}}>
                <input type="file" style={{ display: 'none'}} />
                <br></br>
                <BackupIcon sx={{position:"relative",left:"47%"}} fontSize="medium" color="action"/>
                <Typography sx={{textAlign:"center"}}>Drag and drop files here or click to browse</Typography>
                <Button variant="contained" sx={{position:"relative",left:"38%" ,textTransform:"capitalize",marginBottom:"1%"}}>
                  Choose Files
                </Button>
                </Box>
                  <br></br>
                <Typography>Key Dates *</Typography>
                <Box sx={{border:"1px solid grey",width:"95%"}}>
                    <Stack direction={"row"} spacing={3} style={{marginTop:"2%",marginLeft:"2%",marginBottom:"2%"}}>
                         <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <DesktopDatePicker slotProps={{ textField: { size: 'small' } }}></DesktopDatePicker>
                        </LocalizationProvider>
                        <TextField size="small"></TextField>
                        <IconButton><AddIcon color="primary"/></IconButton>
                        <IconButton style={{position:"relative",right:"4%"}}><DeleteIcon color="error"/></IconButton>
                    </Stack>
                </Box>
                  <br></br>
                <Typography>Update Log</Typography>
                <Box sx={{border:"1px solid grey",width:"95%"}}>
                    <Stack direction={"row"} style={{marginTop:"2%",marginLeft:"2%",marginBottom:"1%"}}>
                    <Typography>Update Type:</Typography>
                    <Autocomplete id='LogType' disablePortal options={['Internal Note','Communication']}  renderInput={(params) => <TextField  sx={{width:"250px",'& .MuiInputBase-input': {height:"5px",boxSizing: 'border-box'}}} {...params}  placeholder="Select Department" required />}  />
                    </Stack>
                    <TextareaAutosize minRows={3}  style={{width:"94%",position:"relative",left:"2%"}}></TextareaAutosize>
                    <Button sx={{position:"relative",left:"2%",marginBottom:"1%",color:"white",width:"30%",textTransform:"capitalize",bgcolor:'rgb(19, 88, 185)'}}>Add Update</Button>
                </Box>
                <br></br>
                <Button sx={{position:"relative",left:"30%",color:"white",width:"30%",textTransform:"capitalize",bgcolor:'rgb(20, 161, 81)'}}>Save</Button>
                <br></br>
                
         </FormControl>
    </Box>)
}