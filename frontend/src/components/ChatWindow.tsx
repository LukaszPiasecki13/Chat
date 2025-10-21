import { useState, useEffect, useRef } from "react";
import {
  Box,
  TextField,
  Button,
  List,
  ListItem,
  Typography,
  Paper,
  Avatar,
  Divider,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import * as api from "../services/api";
import type { Message, User } from "../types";

interface ChatWindowProps {
  currentUser: User;
  receiver: User;
}

export function ChatWindow({ currentUser, receiver }: ChatWindowProps) {
  const roomName = "test";

  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");

  const socketRef = useRef<WebSocket | null>(null);
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const loadMessages = async () => {
      setMessages([]);
      try {
        const historicalMessages = await api.getConversation(
          currentUser.id,
          receiver.id
        );
        setMessages(historicalMessages);
      } catch (error) {
        console.error("Failed to load historical messages:", error);
      }
    };

    loadMessages();

    const socket = api.connectWebSocket(roomName, (message) => {
      setMessages((prev) => [...prev, message]);
    });
    socketRef.current = socket;

    return () => {
      socket.close();
    };
  }, [currentUser.id, receiver.id, roomName]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = () => {
    if (inputValue.trim() && socketRef.current?.readyState === WebSocket.OPEN) {
      const messagePayload = {
        message: inputValue,
        sender_id: currentUser.id,
        receiver_id: receiver.id,
      };
      socketRef.current.send(JSON.stringify(messagePayload));
      setInputValue("");
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Paper
      square
      elevation={0}
      sx={{ height: "100%", display: "flex", flexDirection: "column", bgcolor: "grey.50" }}
    >
      <Box sx={{ p: 2, display: "flex", alignItems: "center", gap: 2 }}>
        <Avatar sx={{ bgcolor: "secondary.main" }}>
          {receiver.username.charAt(0).toUpperCase()}
        </Avatar>
        <Typography variant="h6">{receiver.username}</Typography>
      </Box>
      <Divider />

      <Box sx={{ flexGrow: 1, overflow: "auto", p: 2 }}>
        <List>
          {messages.map((msg, index) => {
            const isMyMessage = msg.sender === currentUser.id;
            return (
              <ListItem
                key={index}
                sx={{
                  display: "flex",
                  justifyContent: isMyMessage ? "flex-end" : "flex-start",
                  p: 0.5,
                }}
              >
                <Box sx={{ maxWidth: "75%", display: "flex", flexDirection: "column" }}>
                  <Typography
                    variant="caption"
                    sx={{
                      alignSelf: isMyMessage ? "flex-end" : "flex-start",
                      color: "text.secondary",
                      mx: 1,
                    }}
                  >
                    {isMyMessage ? "You" : `User ${msg.sender}`}
                  </Typography>

                  <Paper
                    elevation={2}
                    sx={{
                      p: 1.5,
                      borderRadius: 4,
                      borderTopLeftRadius: isMyMessage ? 16 : 0,
                      borderTopRightRadius: isMyMessage ? 0 : 16,
                      bgcolor: msg.isError
                        ? "error.main"
                        : isMyMessage
                        ? "primary.main"
                        : "background.paper",
                      color: msg.isError
                        ? "error.contrastText"
                        : isMyMessage
                        ? "primary.contrastText"
                        : "text.primary",
                    }}
                  >
                    <Typography variant="body1">{msg.content}</Typography>
                  </Paper>

                  <Typography
                    variant="caption"
                    sx={{
                      alignSelf: isMyMessage ? "flex-end" : "flex-start",
                      color: "text.secondary",
                      mt: 0.5,
                      mx: 1,
                    }}
                  >
                    {new Date(msg.timestamp ?? "").toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </Typography>
                </Box>
              </ListItem>
            );
          })}
          <div ref={chatEndRef} />
        </List>
      </Box>

      <Divider />

      <Box
        component="form"
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage();
        }}
        sx={{ display: "flex", alignItems: "center", p: 2 }}
      >
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type your message..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          sx={{
            mr: 1,
            "& .MuiOutlinedInput-root": { borderRadius: "20px" },
          }}
        />
        <Button
          type="submit"
          variant="contained"
          endIcon={<SendIcon />}
          disabled={!inputValue.trim()}
          sx={{ borderRadius: "20px", px: 3 }}
        >
          Send
        </Button>
      </Box>
    </Paper>
  );
}