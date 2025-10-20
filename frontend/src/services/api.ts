import axios from "axios";
import type { User, Message } from "../types";

const apiClient = axios.create({
  baseURL: "http://localhost:8000/",
  
});

const getAuthHeaders = (userId: number) => ({
  headers: { "X-User-ID": userId },
});

export const getUser = async (userId: number): Promise<User> => {
  const response = await apiClient.get<User>(
    `/api/users/${userId}/`,
    getAuthHeaders(userId)
  );
  return response.data;
};

export const getUsers = async (currentUserId: number): Promise<User[]> => {
  const response = await apiClient.get<User[]>(
    "/api/users/",
    getAuthHeaders(currentUserId)
  );
  return response.data;
};

export const getConversation = async (
  currentUserId: number,
  receiverId: number
): Promise<Message[]> => {
  const response = await apiClient.get<Message[]>(
    `/api/conversation/${receiverId}/`,
    getAuthHeaders(currentUserId)
  );
  if (!response.status.toString().startsWith("2")) {
    throw new Error(`Network response was not ok: ${response.statusText}`);
  }
  return response.data;
};

export const sendMessage = async (
  currentUserId: number,
  receiverId: number,
  content: string
): Promise<Message> => {
  const payload = { receiver_id: receiverId, content };
  const response = await apiClient.post<Message>(
    "/api/messages/create/",
    payload,
    getAuthHeaders(currentUserId)
  );
  return response.data;
};

export const connectWebSocket = (
  roomName: string,
  onMessage: (message: Message) => void
) => {
  const socket = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${roomName}/`);

  socket.onopen = () => console.log("WebSocket connected");
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
  if (data.error) {
    const errorMessage: Message = {
      content: data.error,
      isError: true,
      timestamp: new Date().toISOString(),
    };
    onMessage(errorMessage);
    return;
  }
    const message: Message = {
      id: data.id,
      sender: data.sender_id,
      receiver: data.receiver_id,
      content: data.message,
      timestamp: data.timestamp,
      isError: false,
    };
    onMessage(message);
  };

  socket.onclose = () => console.log("WebSocket closed");
  socket.onerror = (e) => console.error("WebSocket error:", e);

  return socket;
};
