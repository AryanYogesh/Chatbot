import React, { useState } from "react";
import { Container, Box, TextField, IconButton, List, ListItem, Typography, Divider } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages([...messages, { text: input, sender: "user" }]);
    setInput("");
    
    // Placeholder for chatbot response (to be integrated with backend)
    setTimeout(() => {
      setMessages((prev) => [...prev, { text: "This is a bot response", sender: "bot" }]);
    }, 1000);
  };

  return (
    <Container maxWidth="md" sx={{ display: "flex", height: "90vh", paddingTop: 2 }}>
      {/* Sidebar */}
      <Box sx={{ width: "25%", borderRight: "1px solid #ccc", padding: 2 }}>
        <Typography variant="h6">Previous Chats</Typography>
        <Divider sx={{ marginY: 1 }} />
        <List>
          <ListItem button>Chat 1</ListItem>
          <ListItem button>Chat 2</ListItem>
        </List>
      </Box>
      
      {/* Chat Window */}
      <Box sx={{ flex: 1, display: "flex", flexDirection: "column", padding: 2 }}>
        <Typography variant="h6" align="center">AI Chatbot</Typography>
        <Divider sx={{ marginY: 1 }} />
        <Box sx={{ flex: 1, overflowY: "auto", padding: 1, border: "1px solid #ccc", borderRadius: 2 }}>
          {messages.map((msg, index) => (
            <Typography key={index} sx={{
              backgroundColor: msg.sender === "user" ? "#e3f2fd" : "#f3e5f5",
              padding: 1,
              borderRadius: 1,
              marginY: 0.5,
              textAlign: msg.sender === "user" ? "right" : "left",
            }}>
              {msg.text}
            </Typography>
          ))}
        </Box>
        
        {/* Input Box */}
        <Box sx={{ display: "flex", marginTop: 2 }}>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <IconButton color="primary" onClick={handleSend}>
            <SendIcon />
          </IconButton>
        </Box>
      </Box>
    </Container>
  );
};

export default Chatbot;
