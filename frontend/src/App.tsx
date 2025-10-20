import { useEffect, useState } from "react";
import { ChatWindow } from "./components/ChatWindow";

import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  CssBaseline,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  type SelectChangeEvent,
  Grid,
  Paper,
  List,
  ListItemButton,
  ListItemText,
  ListItemAvatar,
  Avatar,
} from "@mui/material";



import * as api from "./services/api";
import type { User } from "./types";


const TESTING_USER_ID = 1; // Temporary user ID, only for testing

function App() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [receiver, setReceiver] = useState<User | null>(null);
  const [users, setUsers] = useState<User[]>([]);

  const handleUserChange = (event: SelectChangeEvent<number>) => {
    const newUserId = Number(event.target.value);
    const newUser = users.find(user => user.id === newUserId) || null;
    setCurrentUser(newUser);

    if (newUser && receiver?.id === newUser.id) {
      const newReceiver = users.find(user => user.id !== newUser.id) || null;
      setReceiver(newReceiver);
    }
  };


  const handleReceiverChange = (user: User) => {
    setReceiver(user);
  };

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const allUsers = await api.getUsers(TESTING_USER_ID);  
        const currentUserResponse = await api.getUser(TESTING_USER_ID);
        const fullUserList = [...allUsers, currentUserResponse];
        setUsers(fullUserList);
      } catch (error) {
        console.error("Failed to fetch users", error);
      }
    };

    fetchUsers();
  }, []);

  return (
    <>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Chat
          </Typography>

          <FormControl variant="standard" sx={{ m: 1, minWidth: 120 }}>
            <InputLabel id="user-select-label" sx={{ color: "white" }}>
              You are
            </InputLabel>
            <Select
              labelId="user-select-label"
              value={currentUser?.id || ""}
              onChange={handleUserChange}
              sx={{ color: "white", "& .MuiSvgIcon-root": { color: "white" } }}
            >
              {users.map((user) => (
                <MenuItem key={user.id} value={user.id}>
                  {user.username}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Toolbar>
      </AppBar>

      <Container
        maxWidth={false}
        sx={{
          height: "calc(100vh - 64px)",
          p: 2,
        }}
      >
        <Grid container spacing={2} sx={{ height: "100%" }}>
          <Grid size={{ xs: 12 , sm:4,  md:3}} >
            <Paper sx={{ height: "100%", overflowY: "auto" }}>
              <List component="nav">
                {users
                  .filter((user) => user.id !== currentUser?.id)
                  .map((user) => (
                    <ListItemButton
                      key={user.id}
                      selected={user.id === receiver?.id}
                      onClick={() => handleReceiverChange(user)}
                    >
                      <ListItemAvatar>
                        <Avatar sx={{ bgcolor: "secondary.main" }}>
                          {user.username.charAt(0)}
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText primary={user.username} />
                    </ListItemButton>
                  ))}
              </List>
            </Paper>
          </Grid>

          <Grid 
            size={{ xs: 12 , sm:4,  md:3}}
            sx={{ height: "100%", display: "flex", flexDirection: "column" }}
          >
            {currentUser?.id && receiver?.id ? (
              <ChatWindow
                key={`${currentUser.id}-${receiver.id}`}
                currentUser={currentUser}
                receiver={receiver}
              />
            ) : (
              <Typography>
                Please select your user and a receiver to start chatting.
              </Typography>
            )}
          </Grid>
        </Grid>
      </Container>
    </>
  );
}

export default App;
