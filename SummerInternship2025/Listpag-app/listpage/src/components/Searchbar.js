import TextField from "@mui/material/TextField";
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Autocomplete from "@mui/material/Autocomplete";
import InputAdornment from '@mui/material/InputAdornment';
import SearchIcon from '@mui/icons-material/Search';
import '../styles/Searchbar.css'
export default function SearchAppBar(){
       return(<Box className='Searchbar' >
          <AppBar position="static" >
            <Toolbar id ='Toolbar2'>
              <TextField slotProps={{input:{startAdornment:<InputAdornment position='start'>
                <SearchIcon/>
              </InputAdornment>},}} placeholder="Search RFP IDs...." id='Search'/>
              <Autocomplete id='DepartmentName' disablePortal options={['IT Department','All Departments','HR Department','Finance','Marketing']} renderInput={(params) => <TextField style={{position:"relative",left:"10%"}} {...params} placeholder="All Departments"  />} />
              <Autocomplete id='Type' disablePortal options={['Services','Licenses','All Types']} renderInput={(params) => <TextField style={{position:"relative",left:"20%"}} {...params} placeholder="All Types" />} />
              <Autocomplete id='Priority' disablePortal options={['High','Low','Medium','All Priorities']} renderInput={(params) => <TextField style={{position:"relative",left:"30%"}} {...params} placeholder="All Priorities" />} />
            </Toolbar>
          </AppBar>
       </Box>)
}