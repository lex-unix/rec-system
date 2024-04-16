import type { issueTypes } from './data/issue-types';

export type User = {
  id: number;
  fullName: string;
  email: string;
};

export type IssueType = keyof typeof issueTypes;

export type Issue = {
  id: number;
  subject: string;
  description: string;
  type: IssueType;
  userId: number;
};
export type SocketData = {
  message: string;
  userId: number;
};

export type Chat = {
  id: number;
  issueId: number;
  createdAt: string;
  messages: Message[];
};

export type Message = {
  id: number;
  chatId: number;
  senderId: number;
  createdAt: string;
  text: string;
};
